import streamlit as st
import base64
import math
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# ✅ Configuración de la página
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
    </style>
""", unsafe_allow_html=True)

# 🧭 Título principal
st.markdown("<h1 style='text-align: center;'>🧭 Calculadora de Desvíos Náuticos (σ)</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### Ingrese los datos en formato grados°,décimas:")

# Función para convertir el formato xxx,x a decimal

def parse_input(value):
    try:
        grados, decimas = map(float, value.strip().split(","))
        return grados + decimas / 10
    except:
        st.error("Formato incorrecto. Use grados,décimas (ej: 123,4)")
        return None

# Entradas
Azv_str = st.text_input("🔹 Azv (Azimut Verdadero) - Grados,décimas", "0,0")
Azgc_str = st.text_input("🔹 Azgc (Azimut del Girocompás) - Grados,décimas", "0,0")
Rgc_str = st.text_input("🔹 Rgc (Rumbo del Girocompás) - Grados,décimas", "0,0")
Rcp_str = st.text_input("🔹 Rcp (Rumbo del Compás Patrón) - Grados,décimas", "0,0")
Dm_str = st.text_input("🔹 Dm (Declinación Magnética) - Grados,décimas", "0,0")

Azv = parse_input(Azv_str)
Azgc = parse_input(Azgc_str)
Rgc = parse_input(Rgc_str)
Rcp = parse_input(Rcp_str)
Dm = parse_input(Dm_str)

# Función para diferencia angular normalizada

def diferencia_angular(a, b):
    return (a - b + 180) % 360 - 180

# Cálculos
if st.button("⚓ Calcular"):
    if None not in (Azv, Azgc, Rgc, Rcp, Dm):
        egc = diferencia_angular(Azv, Azgc)
        Rv = (Rgc + egc) % 360
        Vt = diferencia_angular(Rv, Rcp)
        delta_cp = Vt - Dm  # NO normalizar esto

        def f(value):
            sign = "-" if value < 0 else ""
            value = abs(value)
            g = int(value)
            d = round((value - g) * 10)
            if d == 10:
                g += 1
                d = 0
            return f"{sign}{g}°,{d}"

        st.markdown("### 📊 Resultados del Cálculo")
        st.success(f"εgc (Azv - Azgc) = **{f(egc)}**")
        st.success(f"Rv (Rgc + εgc) = **{f(Rv)}**")
        st.success(f"Vt (Rv - Rcp) = **{f(Vt)}**")

        if abs(delta_cp) > 1.5:
            st.markdown(f"""
            <div class='warning'>
            δcp (Vt - Dm) = <strong>{f(delta_cp)}</strong> ⚠️<br>
            ¡ATENCIÓN! El desvío del compás patrón excede el límite recomendado de ±1°,5
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success(f"δcp (Vt - Dm) = **{f(delta_cp)}**")

# 🖋️ Firma
st.markdown("""
    <div class="custom-footer">
        Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
        © 2025 - Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)

