import streamlit as st

# 🎨 Estilos personalizados y firma flotante
st.markdown("""
    <style>
        /* Fondo principal */
        .main {
            background-color: #1e1e1e;
            color: white;
        }

        /* Inputs */
        input {
            background-color: #222 !important;
            color: white !important;
        }

        /* Botón personalizado */
        .stButton > button {
            background-color: #00ccff;
            color: white;
            border-radius: 10px;
            padding: 8px 20px;
            font-weight: bold;
        }

        /* Ocultar footer de Streamlit */
        footer {
            visibility: hidden;
        }

        /* Tu firma flotante */
        .custom-footer {
            position: fixed;
            bottom: 10px;
            right: 20px;
            color: #888;
            font-size: 13px;
        }
    </style>

    <div class="custom-footer">
        Desarrollado con 💙 por Matías Quiroga
    </div>
""", unsafe_allow_html=True)

# Configuración general de la página
st.set_page_config(page_title="Calculadora Náutica", page_icon="🧭", layout="centered")

# Título con estilo
st.markdown("<h1 style='text-align: center; color: navy;'>🧭 Calculadora de Desvíos Náuticos</h1>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("### Ingrese los datos en grados decimales:")

# Entradas
Azv = st.number_input("🔹 Azv (Azimut Verdadero)", value=0.0)
Azgc = st.number_input("🔹 Azgc (Azimut del Girocompás)", value=0.0)
Rgc = st.number_input("🔹 Rgc (Rumbo del Girocompás)", value=0.0)
Rcp = st.number_input("🔹 Rcp (Rumbo del Compás Patrón)", value=0.0)
Dm = st.number_input("🔹 Dm (Declinación Magnética)", value=0.0)

# Cálculos
def calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm):
    egc = Azv - Azgc           # Desvío del girocompás (εgc)
    Rv = Rgc + egc             # Rumbo verdadero estimado
    Vt = Rv - Rcp              # Variación total
    delta_cp = Vt - Dm         # Desvío del compás patrón (δcp)
    return egc, Rv, Vt, delta_cp

if st.button("⚓ Calcular"):
    egc, Rv, Vt, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm)
    
    st.markdown("### 📊 Resultados del Cálculo")
    st.success(f"εgc (Azv - Azgc) = **{egc:.2f}°**")
    st.success(f"Rv (Rgc + εgc) = **{Rv:.2f}°**")
    st.success(f"Vt (Rv - Rcp) = **{Vt:.2f}°**")
    st.success(f"δcp (Vt - Dm) = **{delta_cp:.2f}°**")

    st.markdown("---")

# Firma estática al final (opcional si ya usás la flotante)
st.markdown("""
<div style='text-align: center; color: gray; font-size: 14px; margin-top: 40px;'>
    Desarrollado por <strong>QUIROGA MATIAS</strong> 🌊<br>
    © 2025 - Todos los derechos reservados.
</div>
""", unsafe_allow_html=True)
