import threading
import time
import datetime
import re
from core.dashboard import app
from core.database import update_db, get_db
from tools.cve_monitor import CVEMonitor
from agents.recon_agent import ReconAgent
from agents.nexus_agent import NexusAgent
from agents.sniffer import VICS_Sniffer
from core.reporter import VIC_Reporter


def extract_ip(text):
    """Extrae la primera IP válida de cualquier texto"""
    match = re.search(r'\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b', str(text))
    if match:
        return match.group(1)
    # Acepta hostnames simples como cctv.htb
    hostname = re.match(r'^([a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,})$', str(text).strip())
    if hostname:
        return hostname.group(1)
    return None


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
            raw_target = get_db().get("current_target", "")

            # Validar antes de procesar
            clean_target = extract_ip(raw_target)
            if clean_target and clean_target != last_target:
                last_target = clean_target
                update_db("current_target", clean_target)  # Limpia el target en DB
                threading.Thread(
                    target=self.execute_full_attack,
                    args=(clean_target,),
                    daemon=True
                ).start()
            time.sleep(2)

    def execute_full_attack(self, target):
        from core.ollama_client import VIC_AI_Client
        from core.database import get_db, update_db

        # Doble validación
        if not extract_ip(target):
            print(f"[!] Target inválido ignorado: {target[:50]}")
            return

        ai = VIC_AI_Client()

        def log(msg):
            logs = get_db().get("logs", [])
            logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {msg}")
            update_db("logs", logs)

        print(f"[*] Despertando cerebro táctico para {target}...")
        log("IA Táctica analizando vector de entrada...")

        # Incluye el nmap raw si ya existe
        recon_data = get_db().get("recon_data", {})
        raw_nmap = recon_data.get("raw_nmap", "Sin datos de escaneo previo.")

        prompt = f"""Objetivo: {target}

Resultado del escaneo Nmap:
{raw_nmap}

Analiza los servicios detectados, identifica versiones vulnerables con CVEs conocidos, 
y da el primer comando concreto a ejecutar. Maximo 300 palabras."""

        analisis_ia = ai.ask_ai(prompt)
        log(f"[IA TÁCTICA]: {analisis_ia}")

        # Recon
        recon = ReconAgent(target)
        recon.scan()

        # Segunda llamada a IA con datos del scan
        recon_data = get_db().get("recon_data", {})
        raw_nmap = recon_data.get("raw_nmap", "")
        if raw_nmap:
            prompt2 = f"""Nmap completado para {target}:
{raw_nmap}

Servicios detectados: {recon_data.get('services', [])}

Con esta informacion concreta, cual es el vector de ataque mas probable y el exploit a usar?"""
            analisis_post_scan = ai.ask_ai(prompt2)
            log(f"[IA POST-SCAN]: {analisis_post_scan}")

        # Nexus
        nexus = NexusAgent(target)
        nexus.forge_admin_token()

        # Reporte
        log("Secuencia finalizada. Generando reporte profesional...")
        reporter = VIC_Reporter()
        path = reporter.generate_professional_report()
        print(f"[+] Reporte generado: {path}")


if __name__ == "__main__":
    vic = VIC_Orchestrator()
    threading.Thread(
        target=lambda: app.run(port=5000, debug=False, use_reloader=False),
        daemon=True
    ).start()
    threading.Thread(target=vic.run_cve_monitor, daemon=True).start()
    vic.run_agent_loop()