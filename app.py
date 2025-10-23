import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", layout="wide")

# Título
st.title("🌱 EcoImpact AI - Calculadora de Impacto Ambiental")
st.markdown("Calcula tu impacto ambiental y visualiza tus emisiones de forma clara y atractiva.")

# --- Formulario de entrada ---
st.header("Introduce los datos de tu empresa")
energia = st.number_input("Consumo de energía (kWh)", min_value=0.0)
combustible = st.number_input("Consumo de combustible (litros)", min_value=0.0)
residuos = st.number_input("Residuos generados (kg)", min_value=0.0)
transporte = st.number_input("Distancia transporte (km)", min_value=0.0)

# --- Factores de emisión ---
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

# --- Cálculo ---
emisiones_energia = energia * FE_ENERGIA
emisiones_combustible = combustible * FE_COMBUSTIBLE
emisiones_residuos = residuos * FE_RESIDUOS
emisiones_transporte = transporte * FE_TRANSPORTE
total_emisiones = emisiones_energia + emisiones_combustible + emisiones_residuos + emisiones_transporte

# --- Mostrar resultados ---
st.subheader("📊 Resultados")
st.markdown(f"<h2 style='color:green;'>Total de emisiones: {round(total_emisiones, 2)} kg CO₂e</h2>", unsafe_allow_html=True)

df = pd.DataFrame({
    "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
    "Emisiones (kg CO₂e)": [emisiones_energia, emisiones_combustible, emisiones_residuos, emisiones_transporte]
})

# Gráfica de barras mejorada
chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X("Categoría", sort=None, title=None),
    y=alt.Y("Emisiones (kg CO₂e)", title="Emisiones (kg CO₂e)"),
    color=alt.Color("Emisiones (kg CO₂e)", scale=alt.Scale(scheme="greens")),
    tooltip=["Categoría", "Emisiones (kg CO₂e)"]
).properties(width=700, height=450)

st.altair_chart(chart, use_container_width=True)

# --- Detalle por categoría ---
st.subheader("Detalle de emisiones por categoría")
st.table(df.style.format({"Emisiones (kg CO₂e)": "{:.2f}"}))
