import requests

class VICNotifier:
    def __init__(self):
        # Reemplaza con tus credenciales reales
        self.api_token = "TU_TELEGRAM_TOKEN_AQUI"
        self.chat_id = "TU_CHAT_ID_AQUI"
        self.base_url = f"https://api.telegram.org/bot{self.api_token}/sendMessage"

    def send_alert(self, message):
        payload = {
            "chat_id": self.chat_id,
            "text": f"🚨 [VIC ALERT] 🚨\n\n{message}",
            "parse_mode": "Markdown"
        }
        try:
            requests.post(self.base_url, json=payload, timeout=5)
        except Exception as e:
            print(f"[x] Error enviando notificación: {e}")

if __name__ == "__main__":
    # Prueba rápida
    notifier = VICNotifier()
    notifier.send_alert("*Vertex Intelligence Core* operativo. Sistema sincronizado.")