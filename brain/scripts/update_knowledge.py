import requests
import json
from core.database import update_db

def fetch_cisa_threats():
    url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
    print("[*] Vertex Core: Sincronizando con base de datos CISA...")
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        vulnerabilities = data.get("vulnerabilities", [])
        
        # Guardamos los últimos 50 en la memoria de entrenamiento
        with open("brain/datasets/training_data.jsonl", "a", encoding="utf-8") as f:
            for v in vulnerabilities[:50]:
                entry = {
                    "source": "CISA_KEV",
                    "cve": v['cveID'],
                    "content": f"Vulnerabilidad en {v['product']}: {v['shortDescription']}. Solución: {v['requiredAction']}"
                }
                f.write(json.dumps(entry) + "\n")
        
        print(f"[+] VIC ha aprendido {len(vulnerabilities[:50])} nuevas amenazas globales.")
        update_db("last_intelligence_sync", v['dateAdded'])
        
    except Exception as e:
        print(f"[!] Error de sincronización: {e}")

if __name__ == "__main__":
    fetch_cisa_threats()