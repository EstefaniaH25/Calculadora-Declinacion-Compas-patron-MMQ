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
        .warning {
            background-color: #ffffcc;
            padding: 10px;
            border-left: 5px solid #ffcc00;
            color: #333;
            font-weight: bold;
        }
        .input-container {
            display: flex;
            align-items: center;
        }
        .input-degree {
            margin-right: 5px;
        }
        .input-decimal {
            margin-left: 5px;
            width: 70px;
        }
    </style>
""", unsafe_allow_html=True)

# 🧭 Título principal con símbolo sigma (σ)
st.markdown("<h1 style='text-align: center;'>🧭 Calculadora de Desvíos Náuticos (σ)</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### Ingrese los datos en formato grados°,décimas:")

# Función para convertir el formato xxx,x a xxx°,x y a valor decimal
def format_to_decimal(input_str):
    try:
        grados, decimas = map(float, input_str.split(","))
        return grados + (decimas / 10), f"{int(grados)}°,{int(decimas)}"
    except ValueError:
        st.error("Formato incorrecto. Use grados,décimas (ej: 123,4)")
        return None, None

# 📥 Entradas del usuario en un solo campo de texto
Azv_str = st.text_input("🔹 Azv (Azimut Verdadero) - Grados,décimas (ej: 123,4)", "70,5")
Azgc_str = st.text_input("🔹 Azgc (Azimut del Girocompás) - Grados,décimas", "70,8")
Rgc_str = st.text_input("🔹 Rgc (Rumbo del Girocompás) - Grados,décimas", "132,5")
Rcp_str = st.text_input("🔹 Rcp (Rumbo del Compás Patrón) - Grados,décimas", "144,6")
Dm_str = st.text_input("🔹 Dm (Declinación Magnética) - Grados,décimas", "-10,5")

# Convertir las entradas a formato decimal y formatearlas
Azv, Azv_formatted = format_to_decimal(Azv_str)
Azgc, Azgc_formatted = format_to_decimal(Azgc_str)
Rgc, Rgc_formatted = format_to_decimal(Rgc_str)
Rcp, Rcp_formatted = format_to_decimal(Rcp_str)
Dm, Dm_formatted = format_to_decimal(Dm_str)

# 🧮 Cálculos
def calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm):
    egc = Azv - Azgc           # Desvío del girocompás (εgc)
    Rv = Rgc + egc             # Rumbo verdadero estimado
    Vt = Rv - Rcp              # Variación total
    delta_cp = Vt - Dm         # Desvío del compás patrón (δcp)
    
    return egc, Rv, Vt, delta_cp

# Función para crear PDF con ReportLab
def crear_pdf(Azv_formatted, Azgc_formatted, Rgc_formatted, Rcp_formatted, Dm_formatted, egc, Rv, Vt, delta_cp, alerta_delta_cp):
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
    
    warning_style = ParagraphStyle(
        'WarningStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.orange,
        spaceAfter=5
    )
    
    # Título con símbolo sigma
    titulo = Paragraph("Calculadora de Desvíos Náuticos (σ)", titulo_style)
    story.append(titulo)
    
    # Fecha y hora
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    fecha = Paragraph(f"Generado el: {fecha_actual}", styles['Italic'])
    story.append(fecha)
    story.append(Spacer(1, 0.5*inch))
    
    # Datos ingresados
    datos_titulo = Paragraph("Datos Ingresados:", subtitulo_style)
    story.append(datos_titulo)
    
    story.append(Paragraph(f"Azv (Azimut Verdadero): {Azv_formatted}", normal_style))
    story.append(Paragraph(f"Azgc (Azimut del Girocompás): {Azgc_formatted}", normal_style))
    story.append(Paragraph(f"Rgc (Rumbo del Girocompás): {Rgc_formatted}", normal_style))
    story.append(Paragraph(f"Rcp (Rumbo del Compás Patrón): {Rcp_formatted}", normal_style))
    story.append(Paragraph(f"Dm (Declinación Magnética): {Dm_formatted}", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # Resultados
    resultados_titulo = Paragraph("Resultados del Cálculo:", subtitulo_style)
    story.append(resultados_titulo)
    
    story.append(Paragraph(f"εgc (Azv - Azgc) = {decimal_to_format(egc)}", normal_style))
    story.append(Paragraph(f"Rv (Rgc + εgc) = {decimal_to_format(Rv)}", normal_style))
    story.append(Paragraph(f"Vt (Rv - Rcp) = {decimal_to_format(Vt)}", normal_style))
    
    # Resaltar desvío del compás patrón si está fuera de rango
    if alerta_delta_cp:
        story.append(Paragraph(f"δcp (Vt - Dm) = {decimal_to_format(delta_cp)} ⚠️ FUERA DE RANGO ACEPTABLE", warning_style))
        story.append(Paragraph("El desvío del compás patrón excede el límite recomendado de ±1°,5", warning_style))
    else:
        story.append(Paragraph(f"δcp (Vt - Dm) = {decimal_to_format(delta_cp)}", normal_style))
    
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
    # Verificar que todos los valores han sido ingresados correctamente
    if Azv is not None and Azgc is not None and Rgc is not None and Rcp is not None and Dm is not None:
        egc, Rv, Vt, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm)
        
        # Verificar si el desvío del compás patrón está fuera de rango
        alerta_delta_cp = abs(delta_cp) > 1.5
        
        st.markdown("### 📊 Resultados del Cálculo")
        st.success(f"εgc (Azv - Azgc) = **{decimal_to_format(egc)}**")
        st.success(f"Rv (Rgc + εgc) = **{decimal_to_format(Rv)}**")
        st.success(f"Vt (Rv - Rcp) = **{decimal_to_format(Vt)}**")
        
        # Mostrar el resultado del desvío del compás patrón con alerta si es necesario
        if alerta_delta_cp:
            st.markdown(f"""
            <div class="warning">
                δcp (Vt - Dm) = <strong>{decimal_to_format(delta_cp)}</strong> ⚠️<br>
                ¡ATENCIÓN! El desvío del compás patrón excede el límite recomendado de ±1°,5
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"δcp (Vt - Dm) = **{decimal_to_format(delta_cp)}**")
        
        st.markdown("---")
        
        try:
            # Generar PDF y crear enlace de descarga
            pdf_bytes = crear_pdf(Azv_formatted, Azgc_formatted, Rgc_formatted, Rcp_formatted, Dm_formatted, egc, Rv, Vt, delta_cp, alerta_delta_cp)
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
