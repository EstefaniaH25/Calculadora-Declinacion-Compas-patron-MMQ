import streamlit as st

def calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm):
    egc = Azv - Azgc           # Desvío del girocompás (εgc)
    Rv = Rgc + egc             # Rumbo verdadero estimado
    Vt = Rv - Rcp              # Variación total
    delta_cp = Vt - Dm         # Desvío del compás patrón (δcp)
    return egc, Rv, Vt, delta_cp

st.title("Calculadora de Desvíos del Girocompás y Compás Patrón")
st.markdown("Ingrese los datos en grados decimales:")

Azv = st.number_input("Azv (Azimut Verdadero)", value=0.0)
Azgc = st.number_input("Azgc (Azimut del Girocompás)", value=0.0)
Rgc = st.number_input("Rgc (Rumbo del Girocompás)", value=0.0)
Rcp = st.number_input("Rcp (Rumbo del Compás Patrón)", value=0.0)
Dm = st.number_input("Dm (Declinación Magnética)", value=0.0)

if st.button("Calcular"):
    egc, Rv, Vt, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Dm)

    st.success("Resultados del Cálculo:")
    st.write(f"εgc (Azv - Azgc) = {egc:.2f}°")
    st.write(f"Rv (Rgc + εgc) = {Rv:.2f}°")
    st.write(f"Vt (Rv - Rcp) = {Vt:.2f}°")
    st.write(f"δcp (Vt - Dm) = {delta_cp:.2f}°")
