import requests
import json
from pathlib import Path
from core.database import update_db
       

class CVEMonitor:
    def __init__(self):
        # En una fase avanzada usaríamos APIs como NVD o CVE Details
        self.critical_threshold = 8.5
        self.keywords = ["FastAPI", "Flask", "Jinja2", "RAG", "Prompt Injection", "Docker"]
        print("[*] Monitor de Amenazas VIC: Escaneando vulnerabilidades 2026...")

    def fetch_latest_cves(self):
        # Simulamos la ingesta de los 59,000 CVEs proyectados para 2026 
        # Aquí VIC busca los CVEs más "calientes" que mencionamos antes
        threat_database = [
            {
                "id": "CVE-2026-23550", 
                "tech": "WordPress Modular DS", 
                "severity": 10.0, 
                "vector": "RCE"
            },
            {
                "id": "CVE-2025-55182", 
                "tech": "Next.js / React", 
                "severity": 10.0, 
                "vector": "Deserialization RCE"
            },
            {
                "id": "CVE-2026-20856", 
                "tech": "Windows WSUS", 
                "severity": 8.1, 
                "vector": "MITM RCE"
            }
        ]

    
        
        relevant_threats = [t for t in threat_database if any(k in t['tech'] or t['severity'] >= self.critical_threshold for k in self.keywords)]
        update_db("latest_threats", relevant_threats)
        return relevant_threats

    def alert_agents(self, threats):
        for threat in threats:
            print(f"[!] ALERTA CRÍTICA: {threat['id']} detectado en {threat['tech']}. Impacto: {threat['vector']}")
            # Aquí se pasaría la data a training_data.jsonl automáticamente

if __name__ == "__main__":
    monitor = CVEMonitor()
    new_hits = monitor.fetch_latest_cves()
    monitor.alert_agents(new_hits)