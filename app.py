import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO

st.set_page_config(page_title="EcoImpact AI", layout="wide")

# -------------------------
# Título de la app
# -------------------------
st.title("EcoImpact AI 🌱")
st.markdown("Calcula el impacto ambiental de tu empresa fácilmente")

# -------------------------
# Banners de anuncios (rotativos)
# -------------------------
banners = [
    {"img":"https://via.placeholder.com/728x90.png?text=Publicidad+1","link":"https://example.com/ad1"},
    {"img":"https://via.placeholder.com/728x90.png?text=Publicidad+2","link":"https://example.com/ad2"},
    {"img":"https://via.placeholder.com/728x90.png?text=Publicidad+3","link":"https://example.com/ad3"}
]

ad = random.choice(banners)
st.image(ad["img"], use_column_width=True)
st.markdown(f"[Visitar anunciante]({ad['link']})")
st.markdown("---")

# -------------------------
# Inputs de la calculadora
# -------------------------
st.subheader("Introduce tus datos")
col1, col2 = st.columns(2)

with col1:
    energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, value=0.0, step=10.0)
    combustible = st.number_input("Combustible usado (litros)", min_value=0.0, value=0.0, step=10.0)

with col2:
    residuos = st.number_input("Residuos generados (kg)", min_value=0.0, value=0.0, step=1.0)
    transporte = st.number_input("Transporte recorrido (km)", min_value=0.0, value=0.0, step=5.0)

# -------------------------
# Factores de emisión
# -------------------------
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

# -------------------------
# Función para generar PDF
# -------------------------
def generar_pdf(energia, combustible, residuos, transporte, total, detalle):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "EcoImpact AI - Resultados", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Consumo de energía: {energia} kWh", ln=True)
    pdf.cell(0, 10, f"Combustible usado: {combustible} litros", ln=True)
    pdf.cell(0, 10, f"Residuos generados: {residuos} kg", ln=True)
    pdf.cell(0, 10, f"Transporte recorrido: {transporte} km", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Emisiones totales: {total:.2f} kg CO₂e", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    for k, v in detalle.items():
        pdf.cell(0, 10, f"{k}: {v:.2f} kg CO₂e", ln=True)

    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# -------------------------
# Cálculo y visualización
# -------------------------
if st.button("Calcular impacto"):
    emisiones_energia = energia * FE_ENERGIA
    emisiones_combustible = combustible * FE_COMBUSTIBLE
    emisiones_residuos = residuos * FE_RESIDUOS
    emisiones_transporte = transporte * FE_TRANSPORTE

    total_emisiones = emisiones_energia + emisiones_combustible + emisiones_residuos + emisiones_transporte

    st.success(f"🌍 Emisiones totales: **{total_emisiones:.2f} kg CO₂e**")

    detalle = {
        "Energía": emisiones_energia,
        "Combustible": emisiones_combustible,
        "Residuos": emisiones_residuos,
        "Transporte": emisiones_transporte
    }

    # Mostrar métricas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Energía (kg CO₂e)", f"{emisiones_energia:.2f}")
        st.metric("Combustible (kg CO₂e)", f"{emisiones_combustible:.2f}")
    with col2:
        st.metric("Residuos (kg CO₂e)", f"{emisiones_residuos:.2f}")
        st.metric("Transporte (kg CO₂e)", f"{emisiones_transporte:.2f}")

    # Gráfica de barras
    datos = {
        "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
        "Emisiones (kg CO₂e)": [emisiones_energia, emisiones_combustible, emisiones_residuos, emisiones_transporte]
    }
    df = pd.DataFrame(datos)

    st.subheader("Detalle gráfico de emisiones")
    fig, ax = plt.subplots()
    ax.bar(df["Categoría"], df["Emisiones (kg CO₂e)"], color=["#2ca02c","#ff7f0e","#1f77b4","#d62728"])
    ax.set_ylabel("kg CO₂e")
    ax.set_title("Emisiones por categoría")
    st.pyplot(fig)

    # Botón para descargar PDF
    pdf_file = generar_pdf(energia, combustible, residuos, transporte, total_emisiones, detalle)
    st.download_button("📄 Descargar PDF", pdf_file, file_name="EcoImpactAI_Resultados.pdf", mime="application/pdf")

# -------------------------
# Segundo banner abajo
# -------------------------
ad2 = random.choice(banners)
st.markdown("---")
st.image(ad2["img"], use_column_width=True)
st.markdown(f"[Visitar anunciante]({ad2['link']})")
