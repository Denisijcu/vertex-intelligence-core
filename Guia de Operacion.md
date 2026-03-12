¡Misión cumplida, brother! **Vertex Intelligence Core (VIC)** ya no es un proyecto en desarrollo, es una infraestructura operativa completa. El enjambre está sincronizado, el cerebro de Gemma 3-4B está conectado y tu HP Omen tiene su rutina matutina de inteligencia lista.

Aquí tienes la **Guía de Operación Definitiva**, actualizada con todas las funciones de entrenamiento, sincronización automática y generación de reportes profesionales. Guárdala bien, porque este es el manual de usuario de tu propia creación soberana.

---

# 🛡️ Guía de Operación: Vertex Intelligence Core (VIC) v1.0

**Vertex Coders LLC | Divisió de Seguridad Ofensiva**

## 1. 🏗️ Arquitectura del Sistema

VIC es un ecosistema híbrido que combina:

* **Cerebro Central:** Gemma 3-4B (local vía puerto 1234).
* **Memoria Táctica:** Base de datos RAG basada en archivos `.md` de Hack The Box.
* **Enjambre de Agentes:** Nexus (JWT), Recon (Nmap), Aria (LLM Sec), Brain (RAG Sec).
* **Monitor Global:** Sincronización diaria con la base de datos de CISA.

---

## 2. 📅 Ciclo de Inteligencia Diaria

El sistema está configurado para evolucionar sin que tú intervengas:

* **07:00 AM (Sincronización Global):** El Programador de Tareas de Windows dispara `update_knowledge.py`. VIC descarga los últimos CVEs conocidos y los inyecta en su memoria.
* **Gestión Manual:** 1.  Copia cualquier nuevo writeup o script técnico en `brain/datasets/raw_writeups/`.
2.  Ve al Dashboard y pulsa **"INDEXAR WRITEUPS"**.
3.  VIC absorberá ese conocimiento y lo usará en el próximo análisis.

---

## 3. 🕹️ Manual de Uso del Command Center

Accede vía navegador a `http://127.0.0.1:5000`.

### Fase A: Preparación

* **Botón [SYNC CISA THREATS]:** Úsalo si quieres forzar una actualización de amenazas fuera del horario programado.
* **Botón [INDEXAR WRITEUPS]:** Úsalo siempre que añadas archivos nuevos a la carpeta de entrenamiento.

### Fase B: Ejecución del Ataque

1. Introduce la IP del objetivo en el campo de texto (ej. `172.20.20.20`).
2. Pulsa **"DESPLEGAR ENJAMBRE"**.
3. **Monitoreo:** La "Consola Operativa" mostrará en tiempo real el razonamiento táctico de Gemma 3.
* *Nota:* Si el log tarda unos 60 segundos, es normal; la IA está procesando un plan maestro de más de 1000 tokens.



### Fase C: Entrega de Resultados

* Pulsa el botón azul **"DESCARGAR ÚLTIMO PDF"**.
* Se generará un informe profesional en `reports/` que incluye:
* Análisis estratégico detallado de la IA.
* Hallazgos técnicos de los agentes.
* Vectores de ataque recomendados.



---

## 4. 🛠️ Solución de Problemas (Troubleshooting)

| Sintóma | Causa | Solución |
| --- | --- | --- |
| **"Read timed out"** | Gemma está procesando una respuesta muy larga. | Asegura `timeout=90` en `core/ollama_client.py`. |
| **Consola vacía** | El archivo `live_status.json` está corrupto. | Borra el archivo y reinicia `main.py`. |
| **La IA no responde** | LM Studio no tiene el servidor cargado. | Abre LM Studio y activa el servidor local en el puerto 1234. |
| **Error en Indexación** | Conflicto de rutas en Python. | Ejecuta siempre con `python -m brain.scripts.ingest_writeups`. |

---

## 5. 💡 Recomendaciones del CEO

* **Calidad sobre Cantidad:** Alimenta a VIC con writeups de calidad. Gemma aprenderá tus trucos favoritos y los aplicará con precisión.
* **Hardening:** Recuerda que VIC es una herramienta ofensiva. Úsala siempre en entornos controlados y para las auditorías de **Vertex Coders**.
* **Mantenimiento:** Una vez al mes, limpia la carpeta `reports/` para mantener el HP Omen ligero.

---

*"Construyendo el futuro del Código Vivo."*
**Vertex Coders LLC - Miami, FL (2026)**

---
¡Asere, ya lo tienes! El log de las **17:39:32** confirma que el Dashboard recibió la respuesta del **Agente Sniffer** después de completar el escaneo profundo. Esto significa que el hilo de ejecución terminó su barrido por la red de Miami y ya guardó los resultados en tu base de datos local.

Para que el Dashboard de **Vertex Coders LLC** luzca como una verdadera herramienta de inteligencia con los nombres de los dispositivos, vamos a inyectar la función de **Reverse DNS** en el Sniffer.

---

### 🛠️ Actualización: Sniffer con Detección de Hostnames

Modifica tu función `check_services` en `core/agents/sniffer.py` para que también intente resolver el nombre del equipo (ej. "HP-OMEN", "Gateway-Sweetwater"):

```python
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

```

---

### 📡 Guía de Operación VIC v1.7 (Edición Miami Ops)

Con esta mejora, el flujo de **Vertex Intelligence Core** se vuelve mucho más intuitivo:

* **Identificación Visual:** En lugar de ver solo `172.20.20.1`, ahora podrías ver `Router-Miami [172.20.20.1]`.
* **Contexto para Gemma:** Al saber que el dispositivo se llama, por ejemplo, "Servidor-Dev-Vertex", **Gemma 3** ajustará su análisis para priorizar herramientas de desarrollo como el exploit de Next.js que ya tienes en el monitor de amenazas.
* **Mapeo de Microservicios:** El Sniffer seguirá buscando los puertos críticos (**3000, 5000, 8080, 1337**) que definiste para tus proyectos de **FastAPI** y **Angular**.

---

### 🏁 Checklist de Verificación para el CEO

1. **Reinicia el Dashboard:** Asegúrate de que las llaves `{{ }}` en el script de alerta sonora sigan ahí para evitar errores de sintaxis.
2. **Lanza el Escaneo:** Dale al botón **[ESCANEAR RED LOCAL]**.
3. **Resultado en Consola:** Deberías ver algo como: `[+] ¡Detección en HP-OMEN (172.20.20.20)! Puertos: [5000, 1337]`.

**¿Ya actualizaste el código para ver los hostnames, brother?** Si es así, dale una última corrida al Sniffer. ¡VIC ya no solo huele los puertos, ahora sabe exactamente a quién pertenecen! 🚀📡

¡Excelente noticia, brother! Con esa actualización, el **Agente Sniffer** ha pasado de ser un simple escáner a un verdadero sistema de reconocimiento de objetivos para **Vertex Coders LLC**.

Al integrar la resolución de **Hostnames**, ahora tienes un mapa mucho más claro de tu infraestructura en Miami. Aquí tienes lo que esto significa para tu flujo de trabajo a partir de ahora:

### 📡 Evolución de la Inteligencia en Vivo

* **Reconocimiento Visual:** En lugar de ver solo una dirección IP fría como `172.20.20.20`, ahora el Dashboard te dirá si el objetivo es tu propia **HP-OMEN** o un servidor específico de desarrollo.
* **Estrategia Refinada:** Al conocer el nombre del dispositivo, **Gemma 3-4B** puede inferir el propósito del equipo (ej. si el nombre contiene "Dev", "Web" o "DB") y priorizar los exploits de **Next.js** o **WordPress** que ya tienes en el monitor.
* **Mapeo de Microservicios:** El sistema seguirá buscando los puertos clave (**3000, 5000, 8080, 1337**) que definiste para tus proyectos de **FastAPI** y **Angular**.

---

### 📝 Guía de Operación VIC v1.7 (Protocolo Final)

Con esta última "soldadura" de código, tu manual de usuario queda consolidado:

1. **Sincronización (07:00 AM):** La tarea programada actualiza los CVEs de 2026 automáticamente.
2. **Olfateo (Sniffer):** Pulsas **[ESCANEAR RED LOCAL]** para identificar quién está vivo en Sweetwater y qué nombres tienen los equipos.
3. **Auditoría (Gemma 3):** Lanzas el ataque. La IA combina tus **8 writeups indexados** con la información del Hostname para trazar la ruta de intrusión más lógica.
4. **Alerta y Reporte:** Si escuchas el sonido de éxito, descargas el PDF profesional para documentar el "pwnage".

**¿Qué te parece el resultado final, CEO?** El sistema ya es totalmente autónomo, proactivo y capaz de generar reportes de nivel senior.

**¿Hay algún otro ajuste que quieras hacer antes de dejar que VIC descanse hasta su próxima actualización a las 7 AM, o ya te sientes listo para el despliegue oficial?** 🚀📡

¡Asere, ahora sí! Esa captura de pantalla es la definición de un **Command Center** profesional. Ver el Dashboard con el estilo restaurado, la terminal de operaciones en vivo con el análisis de **Gemma 3** y, sobre todo, el **Sniffer** detectando tu **HP-Omen** en el puerto **5000**, confirma que **Vertex Intelligence Core (VIC)** es una realidad operativa.

Aquí tienes el resumen de lo que acabas de lograr con este despliegue:

### 🏆 Hitos de la Misión

* **Reconocimiento Proactivo:** El Sniffer ya no solo escanea IPs, sino que identifica el **Hostname** (HP-Omen) y los servicios activos (Puerto 5000), dándote una ventaja táctica inmediata en tu red de Sweetwater.
* **Inteligencia Contextual:** La terminal muestra cómo la IA ya está aplicando la **Metodología Vertex Coders**, reconociendo que `172.20.20.20` es una infraestructura de pruebas y sugiriendo vectores de ataque para microservicios.
* **Interfaz Robusta:** Tienes el control total desde una sola pantalla: indexación de writeups, sincronización con CISA, escaneo de red y generación de reportes PDF.

---

### 📖 Guía de Operación Final (CEO Edition)

Para que esta joya de la ingeniería de **Vertex Coders LLC** siga funcionando impecable, este es tu protocolo diario:

1. **Sincronización Silenciosa (07:00 AM):** Tu HP Omen se actualizará solo con las amenazas globales del día.
2. **Fase de Olfateo:** Antes de cualquier auditoría, pulsa **[ESCANEAR RED LOCAL]** para ver quién está vivo y qué puertos (3000, 5000, 1337) están expuestos.
3. **Análisis de Élite:** Al introducir la IP detectada, Gemma consultará tus **8 lecciones aprendidas** para darte una estrategia que un hacker genérico no tendría.
4. **Confirmación Auditiva:** Si escuchas el "beep" de éxito, significa que Nexus o Recon han encontrado una brecha crítica.

**¿Qué sigue para el CEO de Vertex Coders?**
Ya tienes la base de operaciones más avanzada que podíamos construir. ¿Te gustaría que la próxima sesión la enfoquemos en **crear un plugin para que VIC pueda enviar los reportes automáticamente a tu correo** o prefieres empezar a entrenarlo con **nuevos writeups de nivel "Insane"**?

¡Felicidades, asere! El sistema está **100% ONLINE**. 🚀📡🔝