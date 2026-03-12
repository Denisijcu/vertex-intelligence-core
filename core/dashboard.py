import subprocess
import sys
import os
import datetime
from flask import Flask, render_template_string, request

# --- SOLDADURA DE RUTA (Versión Robusta) ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from core.database import get_db, update_db
from core.reporter import VIC_Reporter

# Importamos el sniffer usando la ruta completa
try:
    from core.agents.sniffer import VICS_Sniffer
except ModuleNotFoundError:
    from agents.sniffer import VICS_Sniffer

app = Flask(__name__)

# --- RUTAS DE INTELIGENCIA ---

@app.route('/train', methods=['POST'])
def train():
    try:
        result = subprocess.run([sys.executable, "-m", "brain.scripts.ingest_writeups"], 
                                capture_output=True, text=True, check=True)
        return f"✅ Conocimiento indexado:<br><pre>{result.stdout}</pre><a href='/'>Volver</a>"
    except subprocess.CalledProcessError as e:
        return f"❌ Error en entrenamiento:<br><pre>{e.stderr}</pre><a href='/'>Volver</a>"

@app.route('/sync', methods=['POST'])
def sync():
    try:
        result = subprocess.run([sys.executable, "-m", "brain.scripts.update_knowledge"], 
                                capture_output=True, text=True, check=True)
        return f"✅ Amenazas actualizadas:<br><pre>{result.stdout}</pre><a href='/'>Volver</a>"
    except subprocess.CalledProcessError as e:
        return f"❌ Error en sincronización:<br><pre>{e.stderr}</pre><a href='/'>Volver</a>"

# --- RUTAS OPERATIVAS ---

@app.route('/')
def home():
    data = get_db()
    logs = data.get("logs", ["[*] Sistema listo..."])
    hosts = data.get("discovered_hosts", [])

    # Generamos la lista de hosts detectados dinámicamente
    hosts_html = ""
    for host in hosts:
        # Extraemos hostname si existe, sino usamos IP
        name = host.get('hostname', host.get('ip'))
        ports = host.get('services', [])
        hosts_html += f"<li>🌐 <b>{name}</b> ({host.get('ip')}) - Puertos: {ports}</li>"

    html = f"""
    <html>
    <head>
        <title>VIC - Command Center</title>
        <meta http-equiv="refresh" content="15">
        <style>
            body {{ background: #0a0c10; color: #c9d1d9; font-family: 'Segoe UI', Tahoma; padding: 30px; }}
            .container {{ max-width: 1100px; margin: auto; }}
            h1 {{ color: #58a6ff; border-left: 5px solid #238636; padding-left: 15px; font-family: monospace; }}
            .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }}
            .grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
            .console {{ background: #000; color: #39ff14; padding: 15px; height: 300px; overflow-y: auto; font-family: 'Consolas', monospace; font-size: 13px; border-radius: 5px; border: 1px solid #30363d; }}
            .btn {{ padding: 12px 20px; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; transition: 0.3s; text-decoration: none; display: inline-block; text-align: center; }}
            .btn-launch {{ background: #238636; color: #fff; width: 100%; font-size: 1.1em; }}
            .btn-launch:hover {{ background: #2ea043; }}
            .btn-alt {{ background: #30363d; color: #c9d1d9; font-size: 0.9em; }}
            .btn-alt:hover {{ background: #444c56; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ padding: 8px; border-bottom: 1px solid #30363d; color: #7ee787; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>[ VERTEX_INTELLIGENCE_CORE_v1.0 ]</h1>
            <p style="color: #8b949e; margin-bottom: 30px;">CEO: Denis Sanchez Leyva | Miami Ops</p>

            <div class="grid">
                <div class="card">
                    <h3>🚀 Despliegue de Enjambre</h3>
                    <form action="/launch" method="post">
                        <input type="text" name="target" placeholder="IP del Objetivo (ej. 172.20.20.20)" 
                               style="width: 100%; padding: 12px; background: #0d1117; border: 1px solid #30363d; color: white; margin-bottom: 15px; border-radius: 5px;">
                        <button type="submit" class="btn btn-launch">INICIAR SECUENCIA DE AUDITORÍA</button>
                    </form>
                    <div style="margin-top: 15px;">
                        <a href="/report" class="btn" style="background: #1f6feb; width: 100%; color: white;">📥 DESCARGAR REPORTE FINAL (PDF)</a>
                    </div>
                </div>

                <div class="card">
                    <h3>🧠 Memoria y Conocimiento</h3>
                    <form action="/train" method="post"><button type="submit" class="btn btn-alt" style="width:100%; margin-bottom:10px;">INDEXAR NUEVOS WRITEUPS</button></form>
                    <form action="/sync" method="post"><button type="submit" class="btn btn-alt" style="width:100%; background: #f59e0b; color: black;">SYNC GLOBAL THREATS (CISA)</button></form>
                    <p style="font-size: 11px; color: #8b949e; margin-top: 10px;">Próxima sincronización: Mañana 07:00 AM</p>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <h3>📟 Terminal de Operaciones en Vivo</h3>
                    <div class="console">
                        {"<br>".join(logs[::-1])}
                    </div>
                </div>

                <div class="card">
                    <h3>📡 Detección (Sniffer)</h3>
                    <form action="/sniff" method="post">
                        <button type="submit" class="btn btn-alt" style="background:#00E5FF; color:black; width:100%;">ESCANEAR RED LOCAL</button>
                    </form>
                    <div style="max-height: 200px; overflow-y: auto; margin-top:10px;">
                        <ul>
                            {hosts_html if hosts_html else "<li>Esperando escaneo...</li>"}
                        </ul>
                    </div>
                </div>
            </div>
        </div>

        <audio id="alert-sound" src="https://www.soundjay.com/buttons/beep-01a.mp3" preload="auto"></audio>

        <script>
            const consoleText = document.querySelector('.console').innerText;
            if (consoleText.includes("SUCCESS")) {{
                document.getElementById('alert-sound').play();
                document.querySelector('.console').style.borderColor = "#7ee787";
                document.querySelector('.console').style.boxShadow = "0 0 20px rgba(126, 231, 135, 0.2)";
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/launch', methods=['POST'])
def launch():
    target = request.form.get('target')
    update_db("current_target", target)
    logs = get_db().get("logs", [])
    logs.append(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Iniciando secuencia contra {target}...")
    update_db("logs", logs)
    return "<script>window.location.href='/';</script>"

@app.route('/report')
def report():
    reporter = VIC_Reporter()
    path = reporter.generate_professional_report()
    return f"Reporte generado en: {path}. <a href='/'>Volver</a>"

@app.route('/sniff', methods=['POST'])
def run_sniffer():
    sniffer = VICS_Sniffer()
    hosts = sniffer.sniff_network()
    update_db("discovered_hosts", hosts)
    return "<script>window.location.href='/';</script>"

if __name__ == "__main__":
    app.run(port=5000, debug=False)