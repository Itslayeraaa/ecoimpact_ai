import streamlit as st

st.title("🌱 EcoImpact AI")
st.write("Calculadora de impacto ambiental de empresas")

energia = st.number_input("Consumo de energía (kWh)", min_value=0.0)
combustible = st.number_input("Combustible usado (litros)", min_value=0.0)
residuos = st.number_input("Residuos generados (kg)", min_value=0.0)
transporte = st.number_input("Distancia transporte (km)", min_value=0.0)

if st.button("Calcular impacto"):
    FE_ENERGIA = 0.233
    FE_COMBUSTIBLE = 2.68
    FE_RESIDUOS = 1.9
    FE_TRANSPORTE = 0.12

    emisiones = (
        energia * FE_ENERGIA +
        combustible * FE_COMBUSTIBLE +
        residuos * FE_RESIDUOS +
        transporte * FE_TRANSPORTE
    )

    st.success(f"Emisiones totales: {emisiones:.2f} kg CO₂e")
    st.write("📊 Detalle por categoría:")
    st.write(f"Energía: {energia*FE_ENERGIA:.2f} kg CO₂e")
    st.write(f"Combustible: {combustible*FE_COMBUSTIBLE:.2f} kg CO₂e")
    st.write(f"Residuos: {residuos*FE_RESIDUOS:.2f} kg CO₂e")
    st.write(f"Transporte: {transporte*FE_TRANSPORTE:.2f} kg CO₂e")
import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoImpact AI", page_icon="🌱", layout="centered")

st.title("🌱 EcoImpact AI")
st.write("Calculadora de impacto ambiental de empresas")

# Entrada de datos
energia = st.number_input("Consumo de energía (kWh)", min_value=0.0)
combustible = st.number_input("Combustible usado (litros)", min_value=0.0)
residuos = st.number_input("Residuos generados (kg)", min_value=0.0)
transporte = st.number_input("Distancia transporte (km)", min_value=0.0)

if st.button("Calcular impacto"):
    # Factores de emisión
    FE_ENERGIA = 0.233
    FE_COMBUSTIBLE = 2.68
    FE_RESIDUOS = 1.9
    FE_TRANSPORTE = 0.12

    # Cálculo de emisiones
    detalle = {
        "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
        "Emisiones (kg CO₂e)": [
            energia*FE_ENERGIA,
            combustible*FE_COMBUSTIBLE,
            residuos*FE_RESIDUOS,
            transporte*FE_TRANSPORTE
        ]
    }
    
    df = pd.DataFrame(detalle)
    total = df["Emisiones (kg CO₂e)"].sum()

    # Resultados
    st.success(f"Emisiones totales: {total:.2f} kg CO₂e")
    st.subheader("📊 Detalle por categoría")
    st.dataframe(df)

    # Gráfico de barras
    st.bar_chart(df.set_index("Categoría"))

