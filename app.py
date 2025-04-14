import streamlit as st

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

# 🔘 Botón de cálculo
if st.button("⚓ Calcular"):
    egc, Rv, Vt, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm)
    
    st.markdown("### 📊 Resultados del Cálculo")
    st.success(f"εgc (Azv - Azgc) = **{egc:.2f}°**")
    st.success(f"Rv (Rgc + εgc) = **{Rv:.2f}°**")
    st.success(f"Vt (Rv - Rcp) = **{Vt:.2f}°**")
    st.success(f"δcp (Vt - Dm) = **{delta_cp:.2f}°**")
    st.markdown("---")

# 🖋️ Firma
st.markdown("""
    <div class="custom-footer">
        Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
        © 2025 - Todos los derechos reservados.
    </div>
""", unsafe_allow_html=True)

