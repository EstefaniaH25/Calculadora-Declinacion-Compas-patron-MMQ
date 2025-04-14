import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Configuración de la app
st.set_page_config(page_title="Calculadora de Desvíos Náuticos (σ)", layout="centered")

# Modo visual
modo = st.selectbox("🎨 Elegí el modo de visualización", ["Claro", "Oscuro"])

if modo == "Oscuro":
    st.markdown("""
        <style>
        body {
            background-color: #1c1c1c;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #333;
            color: white;
        }
        .stButton > button {
            background-color: #444;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# Título principal
st.markdown("<h2 style='text-align: center;'>⚓ Calculadora de Desvíos Náuticos (σ)</h2>", unsafe_allow_html=True)

# Conversor string "123,4" a decimal
def str_to_decimal(value):
    try:
        return float(value.replace(",", "."))
    except:
        return None

# Entradas de datos
azv_input = st.text_input("🔹 Azv (Azimut Verdadero) - Grados,décimas (ej: 123,4)", "")
azgc_input = st.text_input("🔹 Azgc (Azimut del Girocompás) - Grados,décimas", "")
rgc_input = st.text_input("🔹 Rgc (Rumbo del Girocompás) - Grados,décimas", "")
rcp_input = st.text_input("🔹 Rcp (Rumbo del Compás Patrón) - Grados,décimas", "")
dm_input = st.text_input("🔹 Dm (Declinación Magnética) - Grados,décimas", "")

if st.button("Calcular"):
    azv = str_to_decimal(azv_input)
    azgc = str_to_decimal(azgc_input)
    rgc = str_to_decimal(rgc_input)
    rcp = str_to_decimal(rcp_input)
    dm = str_to_decimal(dm_input)

    if None in (azv, azgc, rgc, rcp, dm):
        st.error("❌ Todos los campos deben estar completos y en el formato correcto.")
    else:
        # Cálculos
        egc = azv - azgc             # εgc
        rv = rgc + egc               # Rv
        vt = rv - rcp                # Vt
        dcp = vt - dm                # δcp

        # Resultados
        st.markdown("### 📊 Resultados del Cálculo")
        st.write(f"εgc (Azv - Azgc) = {egc:.1f}")
        st.write(f"Rv (Rgc + εgc) = {rv:.1f}")
        st.write(f"Vt (Rv - Rcp) = {vt:.1f}")
        st.write(f"δcp (Vt - Dm) = {dcp:.1f}")

        if abs(dcp) > 1.5:
            st.warning("⚠️ ¡ATENCIÓN! El desvío del compás patrón excede el límite recomendado de ±1°,5")

        # Generación de PDF
        def generar_pdf():
            buffer = BytesIO()
            c = canvas.Canvas(buffer, pagesize=letter)
            c.setFont("Helvetica", 12)
            c.drawString(100, 750, "📄 Resultados del Cálculo de Desvíos Náuticos")
            c.drawString(100, 720, f"εgc (Azv - Azgc) = {egc:.1f}")
            c.drawString(100, 700, f"Rv (Rgc + εgc) = {rv:.1f}")
            c.drawString(100, 680, f"Vt (Rv - Rcp) = {vt:.1f}")
            c.drawString(100, 660, f"δcp (Vt - Dm) = {dcp:.1f}")
            if abs(dcp) > 1.5:
                c.setFillColorRGB(1, 0, 0)
                c.drawString(100, 630, "⚠️ ¡El desvío del compás patrón excede el límite recomendado!")
            c.save()
            buffer.seek(0)
            return buffer

        pdf = generar_pdf()
        st.download_button("📥 Descargar PDF", data=pdf, file_name="resultados_navegacion.pdf", mime="application/pdf")

# 🖋️ Firma
st.markdown("""
    <div class="custom-footer">
        Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
        © 2025 - Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)
