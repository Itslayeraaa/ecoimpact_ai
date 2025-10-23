import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", page_icon="🌱", layout="centered")

st.title("🌱 EcoImpact AI")
st.write("Calculadora de impacto ambiental de empresas")

# Entradas de usuario
energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, key="energia")
combustible = st.number_input("Combustible usado (litros)", min_value=0.0, key="combustible")
residuos = st.number_input("Residuos generados (kg)", min_value=0.0, key="residuos")
transporte = st.number_input("Distancia transporte (km)", min_value=0.0, key="transporte")

# Botón para calcular
if st.button("Calcular impacto"):
    # Factores de emisión
    FE_ENERGIA = 0.233
    FE_COMBUSTIBLE = 2.68
    FE_RESIDUOS = 1.9
    FE_TRANSPORTE = 0.12

    # Cálculo de emisiones por categoría
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

