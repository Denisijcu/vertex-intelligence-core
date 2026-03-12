import subprocess
import datetime
from core.database import update_db

class ReconAgent:
    def __init__(self, target_ip):
        self.target_ip = target_ip
        self.found_services = []

    def scan(self):
        print(f"[*] Recon Agent: Escaneando {self.target_ip}...")
        try:
            # Ejecución de Nmap (Asegúrate de tenerlo en el PATH de Windows)
            output = subprocess.check_output(f"nmap -sV --top-ports 1000 {self.target_ip}", shell=True).decode()
            self.analyze(output)
        except Exception as e:
            print(f"[x] Error en escaneo: {e}. Asegúrate de tener Nmap instalado.")
            # Si falla nmap, al menos reportamos el error al Dashboard
            update_db("recon_status", {"status": "ERROR", "msg": "Nmap no encontrado"})

    def analyze(self, data):
        # Lógica de detección basada en tus éxitos de HTB
        if "3000" in data or "Werkzeug" in data:
            self.found_services.append("Flask/Boutique (AlterEgo/NexusAI)")
        if "1337" in data or "Uvicorn" in data:
            self.found_services.append("FastAPI/RAG (VertexBrain)")
        if "Jinja2" in data:
            self.found_services.append("Jinja2 Templates (Prompted)")
            
        print(f"[+] Servicios detectados: {self.found_services}")
        
        # ACTUALIZACIÓN DINÁMICA: Mandamos los hallazgos al Dashboard
        update_db("recon_data", {
            "target": self.target_ip,
            "services": self.found_services,
            "last_scan": datetime.datetime.now().strftime("%H:%M:%S")
        })

if __name__ == "__main__":
    # Prueba con una IP local o de la VPN de HTB
    recon = ReconAgent("127.0.0.1")
    recon.scan()