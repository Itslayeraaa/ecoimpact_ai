import streamlit as st
import pandas as pd
import altair as alt

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", page_icon="🌱", layout="centered")

# Título y descripción
st.markdown(
    "<h1 style='color: #2E8B57; font-family: Arial; text-align: center;'>🌱 EcoImpact AI</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='color: #555555; font-family: Arial; text-align: center;'>Calculadora de impacto ambiental de empresas con simulación de reducción de emisiones</p>",
    unsafe_allow_html=True
)

# --- Entradas de usuario ---
st.subheader("📥 Datos de la empresa")
energia = st.number_input("Consumo de energía (kWh/mes)", min_value=0.0, key="energia", value=1200.0)
combustible = st.number_input("Combustible usado (litros/mes)", min_value=0.0, key="combustible", value=50.0)
residuos = st.number_input("Residuos generados (kg/mes)", min_value=0.0, key="residuos", value=150.0)
transporte = st.number_input("Distancia transporte (km/mes)", min_value=0.0, key="transporte", value=300.0)

# --- Simulación de reducción ---
st.subheader("⚡ Simulación de reducción de emisiones")
reduccion_energia = st.slider("Reducir consumo de energía (%)", 0, 50, 0, key="reduccion_energia")
reduccion_combustible = st.slider("Reducir combustible (%)", 0, 50, 0, key="reduccion_combustible")
reduccion_residuos = st.slider("Reducir residuos (%)", 0, 50, 0, key="reduccion_residuos")
reduccion_transporte = st.slider("Reducir transporte (%)", 0, 50, 0, key="reduccion_transporte")

# Aplicar reducciones
energia *= (1 - reduccion_energia/100)
combustible *= (1 - reduccion_combustible/100)
residuos *= (1 - reduccion_residuos/100)
transporte *= (1 - reduccion_transporte/100)

# --- Botón para calcular ---
if st.button("💚 Calcular impacto"):
    # Factores de emisión
    FE_ENERGIA = 0.233
    FE_COMBUST_


