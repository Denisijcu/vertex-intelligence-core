from fpdf import FPDF
from core.database import get_db
import datetime
import os

class VIC_Reporter:
    def __init__(self):
        self.data = get_db()
        self.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # Aseguramos que la carpeta de reportes exista
        if not os.path.exists("reports"):
            os.makedirs("reports")

    def generate_professional_report(self):
        target = self.data.get("current_target", "172.20.20.20")
        nexus = self.data.get("nexus_status", {})
        recon = self.data.get("recon_data", {})
        logs = self.data.get("logs", [])
        
        # Buscamos el análisis de la IA en los logs
        ai_analysis = next((msg.replace("[IA TÁCTICA]: ", "") for msg in logs if "[IA TÁCTICA]" in msg), "No se generó análisis táctico.")

        pdf = FPDF()
        pdf.add_page()
        
        # --- ENCABEZADO PROFESIONAL ---
        pdf.set_font("Arial", 'B', 16)
        pdf.set_text_color(33, 150, 243) # Azul Vertex
        pdf.cell(0, 10, "VERTEX CODERS LLC - INFORME DE INTELIGENCIA", ln=True, align='C')
        pdf.set_font("Arial", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 10, f"Generado por: VIC (Vertex Intelligence Core) v1.0-PRO", ln=True, align='C')
        pdf.ln(10)

        # --- DATOS DEL OBJETIVO ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Objetivo Auditado: {target}", ln=True)
        pdf.cell(0, 10, f"Fecha de Operación: {self.date}", ln=True)
        pdf.ln(5)

        # --- ANÁLISIS TÁCTICO DE LA IA (Gemma 3) ---
        pdf.set_fill_color(240, 240, 240)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "1. ANALISIS ESTRATEGICO (Gemma 3-4B):", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)
        pdf.multi_cell(0, 6, ai_analysis)
        pdf.ln(5)

        # --- RESULTADOS TÉCNICOS ---
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, "2. HALLAZGOS TÉCNICOS:", ln=True, fill=True)
        pdf.set_font("Arial", size=10)
        pdf.ln(2)
        pdf.cell(0, 10, f"- Agente Nexus: {nexus.get('status', 'N/A')} (Ataque JWT Algorithm Confusion)", ln=True)
        pdf.cell(0, 10, f"- Servicios Detectados: {', '.join(recon.get('services', []))}", ln=True)
        
        # --- CIERRE ---
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 8)
        pdf.cell(0, 10, "CONFIDENCIAL - PROPIEDAD DE VERTEX CODERS LLC", align='C')

        report_name = f"reports/Reporte_VIC_{target.replace('.', '_')}.pdf"
        pdf.output(report_name)
        return report_name

if __name__ == "__main__":
    rep = VIC_Reporter()
    print(f"[+] Reporte generado en: {rep.generate_professional_report()}")