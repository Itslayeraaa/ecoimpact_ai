import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", layout="wide")

st.title("🌱 EcoImpact AI - Calculadora de Impacto Ambiental")
st.markdown("Calcula tu impacto ambiental con todas las funcionalidades disponibles. Gratis para todos los usuarios.")

# --- Espacio para anuncios ---
st.subheader("📢 Anuncios")
st.info("Este espacio puede usarse para banners, enlaces o mensajes publicitarios.")

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
st.metric("Emisiones totales (kg CO₂e)", round(total_emisiones, 2))

df = pd.DataFrame({
    "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
    "Emisiones (kg CO₂e)": [emisiones_energia, emisiones_combustible, emisiones_residuos, emisiones_transporte]
})

chart = alt.Chart(df).mark_bar().encode(
    x="Categoría",
    y="Emisiones (kg CO₂e)",
    color=alt.Color("Emisiones (kg CO₂e)", scale=alt.Scale(scheme="greens"))
).properties(width=600, height=400)

st.altair_chart(chart, use_container_width=True)

# --- Información de planes (solo como referencia) ---
st.markdown("---")
st.subheader("Funcionalidades incluidas (basadas en todos los planes)")

st.write("""
- ✅ Calculadora de emisiones de energía, combustible, residuos y transporte  
- ✅ Gráficas de barras para visualizar el impacto  
- ✅ Exportar resultados a PDF (simulado en versión gratuita)  
- ✅ Análisis de reducción de impacto (simulado)  
- ✅ Información resumida de las emisiones por categoría  
- ✅ Posibilidad de incluir anuncios o patrocinadores  
""")

st.markdown("**Nota:** Todas estas funciones están disponibles sin necesidad de suscripción mensual. Puedes disfrutar de la experiencia completa de manera gratuita.")
