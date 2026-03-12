import threading
import time
import datetime
from core.dashboard import app
from core.database import update_db, get_db
from tools.cve_monitor import CVEMonitor
from agents.recon_agent import ReconAgent
from agents.nexus_agent import NexusAgent
from agents.sniffer import VICS_Sniffer
from core.reporter import VIC_Reporter


class VIC_Orchestrator:
    def __init__(self):
        print("--- Iniciando Vertex Intelligence Core ---")

    def run_cve_monitor(self):
        monitor = CVEMonitor()
        while True:
            threats = monitor.fetch_latest_cves()
            update_db("latest_threats", threats)
            time.sleep(300)

    def run_agent_loop(self):
        last_target = ""
        while True:
            target = get_db().get("current_target", "")
            if target and target != last_target:
                last_target = target
                # Lanzamos el ataque en un hilo separado para no bloquear el loop
                threading.Thread(target=self.execute_full_attack, args=(target,)).start()
            time.sleep(2)

    def execute_full_attack(self, target):
        from core.ollama_client import VIC_AI_Client
        from core.database import get_db, update_db
        
        ai = VIC_AI_Client()
        logs = get_db().get("logs", [])
        
        # --- EL CABLE RECONECTADO: LLAMADA A LA IA ---
        print(f"[*] Despertando cerebro táctico para {target}...")
        logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] IA Táctica analizando vector de entrada...")
        update_db("logs", logs)

        # Le pasamos tus writeups (opcional: podrías leer el training_data.jsonl aquí)
        analisis_ia = ai.ask_ai(f"Analiza el objetivo {target}. Revisa posibles fallos en microservicios y sugiere una ruta de ataque basada en la metodología de Vertex Coders.")
        
        # Guardamos la respuesta de la IA inmediatamente
        logs = get_db().get("logs", [])
        logs.append(f"[IA TÁCTICA]: {analisis_ia}")
        update_db("logs", logs)
        # --------------------------------------------

        # Ahora siguen los agentes...
        target_ip = target.replace("http://", "").split(":")[0].split("/")[0]
        recon = ReconAgent(target_ip)
        recon.scan()
        
        nexus = NexusAgent(target)
        nexus.forge_admin_token()
        
        # Generación de reporte final
        logs = get_db().get("logs", [])
        logs.append(f"[*] Secuencia finalizada. Generando reporte profesional...")
        update_db("logs", logs)
        
        reporter = VIC_Reporter()
        reporter.generate_professional_report()

if __name__ == "__main__":
    vic = VIC_Orchestrator()
    threading.Thread(target=lambda: app.run(port=5000, debug=False, use_reloader=False), daemon=True).start()
    threading.Thread(target=vic.run_cve_monitor, daemon=True).start()
    vic.run_agent_loop()