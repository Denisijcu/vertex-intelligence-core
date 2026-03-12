import scapy.all as scapy
import socket
import os

class VICS_Sniffer:
    def __init__(self, target_range="172.20.20.0/24"):
        self.target_range = target_range
        # Puertos críticos basados en tus proyectos de Vertex Coders
        self.critical_ports = [80, 443, 3000, 5000, 8080, 1337]

    def sniff_network(self):
        print(f"[*] Sniffer: Iniciando escaneo profundo en {self.target_range}...")
        discovered_hosts = []
        
        # 1. Intento de escaneo ARP (Requiere ejecutar como Administrador)
        try:
            ans, _ = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff")/scapy.ARP(pdst=self.target_range), 
                               timeout=2, verbose=False)
            for _, received in ans:
                ip = received.psrc
                services = self.check_services(ip)
                if services:
                    discovered_hosts.append({"ip": ip, "services": services})
        except Exception as e:
            print(f"[!] Error en ARP: {e}. Pasando a escaneo directo de sockets...")

        # 2. Escaneo Directo de Sockets (Si ARP no encuentra nada)
        if not discovered_hosts:
            base_ip = ".".join(self.target_range.split(".")[:-1]) + "."
            # Escaneamos las IPs más probables primero (.1 gateway, .20 tú, etc)
            for i in range(1, 255):
                ip = f"{base_ip}{i}"
                services = self.check_services(ip)
                if services:
                    print(f"[+] ¡Detección en {ip}! Puertos: {services}")
                    discovered_hosts.append({"ip": ip, "services": services})
        
        return discovered_hosts

    def check_services(self, ip):
            found = []
            hostname = "Desconocido"
            
            # Intento de resolución de nombre (Hostname)
            try:
                hostname = socket.gethostbyaddr(ip)[0]
            except socket.herror:
                hostname = ip # Si no hay nombre, usamos la IP como etiqueta

            for port in self.critical_ports:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(0.1)
                    if s.connect_ex((ip, port)) == 0:
                        found.append(port)
            
            return {"ports": found, "hostname": hostname} if found else None