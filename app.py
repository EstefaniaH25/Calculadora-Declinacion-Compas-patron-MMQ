import streamlit as st
import base64
from datetime import datetime
from fpdf import FPDF

# ✅ Configuración de la página (¡esto va primero!)
st.set_page_config(page_title="Calculadora Náutica", page_icon="🧭", layout="centered")

# 🎨 Estilos personalizados y firma flotante
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', sans-serif;
        }
        h1 {
            color: navy;
        }
        .custom-footer {
            text-align: center;
            color: gray;
            font-size: 14px;
            margin-top: 50px;
        }
        .stButton>button {
            background-color: #004080;
            color: white;
            border-radius: 8px;
            padding: 0.5em 1.5em;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #0066cc;
        }
        .download-button {
            text-align: center;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Título principal
st.markdown("<h1 style='text-align: center;'>🧭 Calculadora de Desvíos Náuticos</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### Ingrese los datos en grados decimales:")

# 📥 Entradas del usuario
Azv = st.number_input("🔹 Azv (Azimut Verdadero)", value=0.0)
Azgc = st.number_input("🔹 Azgc (Azimut del Girocompás)", value=0.0)
Rgc = st.number_input("🔹 Rgc (Rumbo del Girocompás)", value=0.0)
Rcp = st.number_input("🔹 Rcp (Rumbo del Compás Patrón)", value=0.0)
Dm = st.number_input("🔹 Dm (Declinación Magnética)", value=0.0)

# 🧮 Cálculos
def calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm):
    egc = Azv - Azgc           # Desvío del girocompás (εgc)
    Rv = Rgc + egc             # Rumbo verdadero estimado
    Vt = Rv - Rcp              # Variación total
    delta_cp = Vt - Dm         # Desvío del compás patrón (δcp)
    return egc, Rv, Vt, delta_cp

# Función para crear PDF (modificada para manejar caracteres Unicode)
def crear_pdf(Azv, Azgc, Rgc, Rcp, Dm, egc, Rv, Vt, delta_cp):
    pdf = FPDF()
    pdf.add_page()
    
    # Configurar para soportar caracteres Unicode
    pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    
    # Alternativa si la fuente DejaVu no está disponible
    try:
        # Título
        pdf.cell(190, 10, "Calculadora de Desvios Nauticos", 0, 1, "C")
    except Exception:
        # Si falla, intentar con Arial
        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "Calculadora de Desvios Nauticos", 0, 1, "C")
    
    pdf.ln(10)
    
    # Fecha y hora
    pdf.set_font("Arial", "I", 10)
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.cell(190, 10, f"Generado el: {fecha_actual}", 0, 1, "R")
    pdf.ln(5)
    
    # Datos ingresados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Datos Ingresados:", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 8, f"Azv (Azimut Verdadero): {Azv:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Azgc (Azimut del Giroscopio): {Azgc:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Rgc (Rumbo del Giroscopio): {Rgc:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Rcp (Rumbo del Compas Patron): {Rcp:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Dm (Declinacion Magnetica): {Dm:.2f} grados", 0, 1, "L")
    pdf.ln(10)
    
    # Resultados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(190, 10, "Resultados del Calculo:", 0, 1, "L")
    pdf.set_font("Arial", "", 12)
    pdf.cell(190, 8, f"egc (Azv - Azgc) = {egc:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Rv (Rgc + egc) = {Rv:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"Vt (Rv - Rcp) = {Vt:.2f} grados", 0, 1, "L")
    pdf.cell(190, 8, f"dcp (Vt - Dm) = {delta_cp:.2f} grados", 0, 1, "L")
    
    # Pie de página
    pdf.ln(20)
    pdf.set_font("Arial", "I", 10)
    pdf.cell(190, 10, "Desarrollado por QUIROGA MATIAS © 2025", 0, 1, "C")
    
    return pdf.output(dest="S").encode("latin1", errors="replace")

# Función para crear enlace de descarga
def get_binary_file_downloader_html(bin_data, file_label='File', filename='file.pdf'):
    bin_str = base64.b64encode(bin_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{filename}">{file_label}</a>'
    return href

# 🔘 Botón de cálculo
if st.button("⚓ Calcular"):
    egc, Rv, Vt, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm)
    
    st.markdown("### 📊 Resultados del Cálculo")
    st.success(f"εgc (Azv - Azgc) = **{egc:.2f}°**")
    st.success(f"Rv (Rgc + εgc) = **{Rv:.2f}°**")
    st.success(f"Vt (Rv - Rcp) = **{Vt:.2f}°**")
    st.success(f"δcp (Vt - Dm) = **{delta_cp:.2f}°**")
    st.markdown("---")
    
    try:
        # Generar PDF y crear enlace de descarga
        pdf_bytes = crear_pdf(Azv, Azgc, Rgc, Rcp, Dm, egc, Rv, Vt, delta_cp)
        fecha_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Resultados_Desvios_Nauticos_{fecha_archivo}.pdf"
        
        st.markdown("<div class='download-button'>", unsafe_allow_html=True)
        download_link = get_binary_file_downloader_html(pdf_bytes, 'Descargar Resultados como PDF', filename)
        st.markdown(download_link, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Hubo un problema al generar el PDF. Por favor intente nuevamente.")
        st.error("Error: Problema con la codificación de caracteres especiales.")

# 🖋️ Firma
st.markdown("""
    <div class="custom-footer">
        Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
        © 2025 - Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)
