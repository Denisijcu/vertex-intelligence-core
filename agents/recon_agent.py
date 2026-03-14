import subprocess
import datetime
import re
from core.database import update_db

class ReconAgent:
    def __init__(self, target_ip):
        # Validación de IP antes de escanear
        self.target_ip = self._validate_ip(target_ip)
        self.found_services = []
        self.raw_output = ""

    def _validate_ip(self, target):
        """Acepta solo IPs válidas o hostnames simples"""
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$')
        hostname_pattern = re.compile(r'^[a-zA-Z0-9\-\.]+$')
        if ip_pattern.match(target) or hostname_pattern.match(target):
            return target
        # Si no es válido, extrae la primera IP del texto
        match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target)
        if match:
            print(f"[!] Target inválido, extrayendo IP: {match.group()}")
            return match.group()
        return "127.0.0.1"

    def scan(self):
        print(f"[*] Recon Agent: Escaneando {self.target_ip}...")
        try:
            output = subprocess.check_output(
                f"nmap -sV --top-ports 1000 {self.target_ip}",
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode(errors='replace')
            self.raw_output = output
            self.analyze(output)
        except Exception as e:
            print(f"[x] Error en escaneo: {e}. Asegúrate de tener Nmap instalado.")
            update_db("recon_status", {"status": "ERROR", "msg": str(e)})

    def analyze(self, data):
        """Detecta servicios reales del output de nmap"""
        service_map = {
            # Web frameworks
            "Werkzeug":         "Flask/Python Web",
            "Uvicorn":          "FastAPI/ASGI",
            "Jinja2":           "Jinja2 Templates",
            "Jetty":            "Java Jetty",
            "Tomcat":           "Apache Tomcat",
            "nginx":            "nginx",
            "Apache":           "Apache httpd",
            "Express":          "Node.js/Express",
            # Databases
            "mysql":            "MySQL",
            "PostgreSQL":       "PostgreSQL",
            "MongoDB":          "MongoDB",
            "redis":            "Redis",
            # Auth / APIs
            "pac4j":            "pac4j JWT",
            "Keycloak":         "Keycloak Auth",
            # CCTV / Media
            "ZoneMinder":       "ZoneMinder CCTV",
            "motionEye":        "motionEye",
            "mediamtx":         "MediaMTX RTSP",
            # CMS
            "WordPress":        "WordPress",
            "Camaleon":         "Camaleon CMS",
            # SSH / infra
            "OpenSSH":          "OpenSSH",
            "MinIO":            "MinIO S3",
        }

        # Detecta por keyword en output
        for keyword, label in service_map.items():
            if keyword.lower() in data.lower():
                self.found_services.append(label)

        # Extrae puertos abiertos
        ports = re.findall(r'(\d+)/tcp\s+open\s+(\S+)', data)
        for port, service in ports:
            entry = f"Port {port}: {service}"
            if entry not in self.found_services:
                self.found_services.append(entry)

        print(f"[+] Servicios detectados: {self.found_services}")

        update_db("recon_data", {
            "target": self.target_ip,
            "services": self.found_services,
            "raw_nmap": self.raw_output,  # Para que Claude lo analice
            "last_scan": datetime.datetime.now().strftime("%H:%M:%S")
        })

if __name__ == "__main__":
    recon = ReconAgent("127.0.0.1")
    recon.scan()