import streamlit as st

def calcular_desvios(Azv, Azgc, Rgc, Rcp, Vt, Dm):
    egc = Azv - Azgc
    egc_cp = Rgc - Rcp
    delta_cp = Vt - (Rcp + Dm)
    return egc, egc_cp, delta_cp

st.title("Calculadora de Desvíos del Girocompás y Compás Patrón")
st.markdown("Ingrese los datos en grados decimales:")

Azv = st.number_input("Azv (Azimut Verdadero)", value=125.25)
Azgc = st.number_input("Azgc (Azimut del Girocompás)", value=123.75)
Rgc = st.number_input("Rgc (Rumbo del Girocompás)", value=98.4)
Rcp = st.number_input("Rcp (Rumbo del Compás Patrón)", value=96.0)
Vt = st.number_input("Vt (Rumbo Verdadero)", value=100.2)
Dm = st.number_input("Dm (Declinación Magnética)", value=4.0)

if st.button("Calcular"):
    egc, egc_cp, delta_cp = calcular_desvios(Azv, Azgc, Rgc, Rcp, Vt, Dm)
    st.success("Resultados del Cálculo:")
    st.write(f"εgc = {egc:.2f}°")
    st.write(f"εgc (compás patrón) = {egc_cp:.2f}°")
    st.write(f"δcp = {delta_cp:.2f}°")
