import streamlit as st
import base64
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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

# Función para crear PDF con ReportLab
def crear_pdf(Azv, Azgc, Rgc, Rcp, Dm, egc, Rv, Vt, delta_cp):
    buffer = io.BytesIO()
    
    # Configurar el documento
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    
    # Estilos
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'TituloStyle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=1,  # Centrado
        spaceAfter=20
    )
    
    subtitulo_style = ParagraphStyle(
        'SubtituloStyle', 
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=10
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        spaceAfter=5
    )
    
    # Título
    titulo = Paragraph("Calculadora de Desvíos Náuticos", titulo_style)
    story.append(titulo)
    
    # Fecha y hora
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha = Paragraph(f"Generado el: {fecha_actual}", styles['Italic'])
    story.append(fecha)
    story.append(Spacer(1, 0.5*inch))
    
    # Datos ingresados
    datos_titulo = Paragraph("Datos Ingresados:", subtitulo_style)
    story.append(datos_titulo)
    
    story.append(Paragraph(f"Azv (Azimut Verdadero): {Azv:.2f}°", normal_style))
    story.append(Paragraph(f"Azgc (Azimut del Girocompás): {Azgc:.2f}°", normal_style))
    story.append(Paragraph(f"Rgc (Rumbo del Girocompás): {Rgc:.2f}°", normal_style))
    story.append(Paragraph(f"Rcp (Rumbo del Compás Patrón): {Rcp:.2f}°", normal_style))
    story.append(Paragraph(f"Dm (Declinación Magnética): {Dm:.2f}°", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Resultados
    resultados_titulo = Paragraph("Resultados del Cálculo:", subtitulo_style)
    story.append(resultados_titulo)
    
    story.append(Paragraph(f"εgc (Azv - Azgc) = {egc:.2f}°", normal_style))
    story.append(Paragraph(f"Rv (Rgc + εgc) = {Rv:.2f}°", normal_style))
    story.append(Paragraph(f"Vt (Rv - Rcp) = {Vt:.2f}°", normal_style))
    story.append(Paragraph(f"δcp (Vt - Dm) = {delta_cp:.2f}°", normal_style))
    
    story.append(Spacer(1, inch))
    
    # Pie de página
    footer = Paragraph("Desarrollado por QUIROGA MATIAS © 2025", styles['Italic'])
    story.append(footer)
    
    # Construir el documento
    doc.build(story)
    
    # Obtener el valor del buffer y devolverlo
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

# Función para crear enlace de descarga
def get_binary_file_downloader_html(bin_data, file_label='File', filename='file.pdf'):
    bin_str = base64.b64encode(bin_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{filename}" class="download-button-link" style="background-color: #004080; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; font-weight: bold;">{file_label}</a>'
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
        download_link = get_binary_file_downloader_html(pdf_bytes, '📥 Descargar Resultados como PDF', filename)
        st.markdown(download_link, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Hubo un problema al generar el PDF. Por favor intente nuevamente.")
        st.error(f"Error: {str(e)}")

# 🖋️ Firma
st.markdown("""
    <div class="custom-footer">
        Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
        © 2025 - Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)
