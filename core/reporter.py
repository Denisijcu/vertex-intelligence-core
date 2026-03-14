from fpdf import FPDF
from core.database import get_db
import datetime
import os
import re


def sanitize(text):
    """Elimina caracteres incompatibles con latin-1"""
    if not isinstance(text, str):
        text = str(text)
    replacements = {
        '\u2014': '-', '\u2013': '-', '\u2012': '-',
        '\u2019': "'", '\u2018': "'",
        '\u201c': '"', '\u201d': '"',
        '\u2026': '...', '\u00b7': '-',
        '\u2022': '-', '\u25cf': '-',
        '\u2264': '<=', '\u2265': '>=',
        '\u00e9': 'e', '\u00f3': 'o', '\u00ed': 'i',
        '\u00e1': 'a', '\u00fa': 'u', '\u00f1': 'n',
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text.encode('latin-1', errors='replace').decode('latin-1')


def sanitize_filename(target):
    """Extrae IP o genera nombre de archivo válido"""
    ip_match = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(target))
    if ip_match:
        return ip_match.group().replace('.', '_')
    clean = re.sub(r'[^\w\-]', '_', str(target)[:30])
    return clean


def section_header(pdf, title):
    """Helper para headers de sección consistentes"""
    pdf.set_fill_color(33, 150, 243)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, sanitize(f"  {title}"), ln=True, fill=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    pdf.ln(2)


class VIC_Reporter:
    def __init__(self):
        self.data = get_db()
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        if not os.path.exists("reports"):
            os.makedirs("reports")

    def generate_professional_report(self):
        # Refresca datos al momento de generar
        self.data = get_db()

        target = self.data.get("current_target", "unknown")
        nexus = self.data.get("nexus_status", {})
        recon = self.data.get("recon_data", {})
        threats = self.data.get("latest_threats", [])
        logs = self.data.get("logs", [])

        # Extrae análisis de IA del log
        ai_analysis = next(
            (msg.replace("[IA TACTICA]: ", "").replace("[IA TÁCTICA]: ", "")
             for msg in reversed(logs) if "[IA TÁCTICA]" in msg or "[IA TACTICA]" in msg),
            "No se genero analisis tactico."
        )

        # Extrae análisis post-scan si existe
        ai_post_scan = next(
            (msg.replace("[IA POST-SCAN]: ", "")
             for msg in reversed(logs) if "[IA POST-SCAN]" in msg),
            None
        )

        pdf = FPDF()
        pdf.set_margins(15, 15, 15)
        pdf.add_page()

        # ── ENCABEZADO ──────────────────────────────────────────
        pdf.set_fill_color(15, 23, 42)
        pdf.rect(0, 0, 210, 35, 'F')
        pdf.set_font("Arial", 'B', 18)
        pdf.set_text_color(33, 150, 243)
        pdf.set_y(8)
        pdf.cell(0, 10, "VERTEX CODERS LLC", ln=True, align='C')
        pdf.set_font("Arial", 'B', 11)
        pdf.set_text_color(200, 200, 200)
        pdf.cell(0, 8, "INFORME DE INTELIGENCIA OFENSIVA", ln=True, align='C')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(15)

        # ── META INFO ────────────────────────────────────────────
        pdf.set_font("Arial", size=10)
        pdf.set_fill_color(245, 245, 245)
        pdf.cell(95, 8, sanitize(f"Objetivo: {target}"), border=1, fill=True)
        pdf.cell(95, 8, sanitize(f"Fecha: {self.date}"), border=1, fill=True, ln=True)
        pdf.cell(95, 8, sanitize(f"Herramienta: VIC v1.0-PRO"), border=1, fill=True)
        pdf.cell(95, 8, sanitize(f"Clasificacion: CONFIDENCIAL"), border=1, fill=True, ln=True)
        pdf.ln(8)

        # ── 1. ANALISIS ESTRATEGICO ──────────────────────────────
        section_header(pdf, "1. ANALISIS ESTRATEGICO - Claude Sonnet 4")
        pdf.multi_cell(0, 6, sanitize(ai_analysis))
        pdf.ln(5)

        # ── 2. ANALISIS POST-SCAN ────────────────────────────────
        if ai_post_scan:
            section_header(pdf, "2. ANALISIS POST-SCAN - Claude Sonnet 4")
            pdf.multi_cell(0, 6, sanitize(ai_post_scan))
            pdf.ln(5)

        # ── 3. HALLAZGOS TECNICOS ────────────────────────────────
        section_header(pdf, "3. HALLAZGOS TECNICOS")

        # Nexus
        nexus_status = nexus.get('status', 'N/A')
        nexus_token = nexus.get('token', '')[:40] + '...' if nexus.get('token') else 'N/A'
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, "Agente Nexus (JWT):", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, sanitize(f"  Estado: {nexus_status}"), ln=True)
        pdf.cell(0, 6, sanitize(f"  Token: {nexus_token}"), ln=True)
        pdf.ln(3)

        # Recon
        services = recon.get('services', [])
        last_scan = recon.get('last_scan', 'N/A')
        pdf.set_font("Arial", 'B', 10)
        pdf.cell(0, 7, "Agente Recon (Nmap):", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.cell(0, 6, sanitize(f"  Ultimo scan: {last_scan}"), ln=True)
        if services:
            for svc in services:
                pdf.cell(0, 6, sanitize(f"  [+] {svc}"), ln=True)
        else:
            pdf.cell(0, 6, "  Sin servicios detectados.", ln=True)
        pdf.ln(5)

        # ── 4. NMAP RAW ──────────────────────────────────────────
        raw_nmap = recon.get('raw_nmap', '')
        if raw_nmap:
            section_header(pdf, "4. OUTPUT NMAP")
            pdf.set_font("Courier", size=8)
            # Limita a primeras 60 lineas para no inflar el PDF
            lines = raw_nmap.split('\n')[:60]
            for line in lines:
                pdf.cell(0, 5, sanitize(line), ln=True)
            pdf.set_font("Arial", size=10)
            pdf.ln(5)

        # ── 5. AMENAZAS CVE ──────────────────────────────────────
        if threats:
            section_header(pdf, "5. AMENAZAS CVE RECIENTES")
            for threat in threats[:5]:
                pdf.cell(0, 6, sanitize(f"  [{threat.get('id', 'N/A')}] {threat.get('title', '')}"), ln=True)
            pdf.ln(5)

        # ── LOG DE OPERACION ─────────────────────────────────────
        section_header(pdf, "6. LOG DE OPERACION")
        pdf.set_font("Courier", size=8)
        for entry in logs[-20:]:  # Ultimas 20 entradas
            if "[IA TÁCTICA]" not in entry and "[IA POST-SCAN]" not in entry:
                pdf.cell(0, 5, sanitize(entry[:100]), ln=True)
        pdf.set_font("Arial", size=10)

        # ── FOOTER ───────────────────────────────────────────────
        pdf.ln(10)
        pdf.set_draw_color(33, 150, 243)
        pdf.line(15, pdf.get_y(), 195, pdf.get_y())
        pdf.ln(3)
        pdf.set_font("Arial", 'I', 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 6, "CONFIDENCIAL - PROPIEDAD DE VERTEX CODERS LLC - Miami, FL 2026", align='C')

        report_name = f"reports/Reporte_VIC_{sanitize_filename(target)}.pdf"
        pdf.output(report_name)
        print(f"[+] Reporte generado: {report_name}")
        return report_name


if __name__ == "__main__":
    rep = VIC_Reporter()
    print(f"[+] Reporte: {rep.generate_professional_report()}")