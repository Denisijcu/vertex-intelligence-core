import requests

class VIC_AI_Client:
    def __init__(self, model="google/gemma-3-4b"):
        self.model = model
        self.url = "http://localhost:1234/api/v1/chat"

    def ask_ai(self, prompt, system_prompt="Eres un experto en ciberseguridad ofensiva."):
        payload = {
            "model": self.model,
            "system_prompt": system_prompt,
            "input": prompt
        }
        try:
            # Subimos el timeout a 90 para darle aire a Gemma
            response = requests.post(self.url, json=payload, timeout=120)
            res_json = response.json()
            # IMPORTANTE: Verifica que esta ruta coincida con el JSON que viste en LM Studio
            return res_json["output"][0]["content"]
        except Exception as e:
            return f"Error de conexión con IA: {e}"