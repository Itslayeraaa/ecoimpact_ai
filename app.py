import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", layout="wide")

# --- Banner de anuncios ---
st.image("https://via.placeholder.com/728x90.png?text=Publicidad+EcoImpact+AI", use_column_width=True)
st.markdown("---")

# Título
st.title("🌱 EcoImpact AI - Calculadora de Impacto Ambiental")
st.markdown("Calcula tu impacto ambiental de forma clara y sencilla.")

# --- Formulario de entrada centrado ---
st.header("Introduce los datos de tu empresa")
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, format="%.2f")
        combustible = st.number_input("Consumo de combustible (litros)", min_value=0.0, format="%.2f")
    
    with col2:
        residuos = st.number_input("Residuos generados (kg)", min_value=0.0, format="%.2f")
        transporte = st.number_input("Distancia transporte (km)", min_value=0.0, format="%.2f")

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

# --- Resultados ---
st.subheader("📊 Resultados")
st.markdown(f"<h2 style='color:green; text-align:center;'>Total de emisiones: {round(total_emisiones, 2)} kg CO₂e</h2>", unsafe_allow_html=True)

df = pd.DataFrame({
    "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
    "Emisiones (kg CO₂e)": [emisiones_energia, emisiones_combustible, emisiones_residuos, emisiones_transporte]
})

# Gráfica de barras centrada y con colores agradables
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
