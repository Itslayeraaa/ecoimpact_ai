import streamlit as st
import pandas as pd
import altair as alt
from fpdf import FPDF
from io import BytesIO

# Configuración de la página
st.set_page_config(page_title="EcoImpact AI", layout="wide")

# --- Banner de anuncios ---
st.image("https://via.placeholder.com/728x90.png?text=Publicidad+EcoImpact+AI", use_column_width=True)
st.markdown("---")

# Título
st.title("🌱 EcoImpact AI - Calculadora de Impacto Ambiental")
st.markdown("Calcula tu impacto ambiental y compáralo con referencias recomendadas.")

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

# --- Benchmark / referencia ---
BENCHMARK = 5000  # kg CO2e recomendado para referencia

# --- Resultados ---
st.subheader("📊 Resultados")
st.markdown(f"<h2 style='color:green; text-align:center;'>Total de emisiones: {round(total_emisiones, 2)} kg CO₂e</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Referencia recomendada: {BENCHMARK} kg CO₂e</p>", unsafe_allow_html=True)

# --- Gráfica comparativa ---
df = pd.DataFrame({
    "Categoría": ["Energía", "Combustible", "Residuos", "Transporte", "Benchmark"],
    "Emisiones (kg CO₂e)": [emisiones_energia, emisiones_combustible, emisiones_residuos, emisiones_transporte, BENCHMARK]
})

chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
    x=alt.X("Categoría", sort=None, title=None),
    y=alt.Y("Emisiones (kg CO₂e)", title="Emisiones (kg CO₂e)"),
    color=alt.Color("Emisiones (kg CO₂e)", scale=alt.Scale(scheme="greens")),
    tooltip=["Categoría", "Emisiones (kg CO₂e)"]
).properties(width=700, height=450)

st.altair_chart(chart, use_container_width=True)

# --- Detalle por categoría ---
st.subheader("Detalle de emisiones por categoría")
st.table(df[:-1].style.format({"Emisiones (kg CO₂e)": "{:.2f}"}))

# --- Generar PDF ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe de Emisiones EcoImpact AI", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Consumo de energía: {energia} kWh", ln=True)
    pdf.cell(0, 10, f"Consumo de combustible: {combustible} litros", ln=True)
    pdf.cell(0, 10, f"Residuos generados: {residuos} kg", ln=True)
    pdf.cell(0, 10, f"Distancia transporte: {transporte} km", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Total emisiones: {round(total_emisiones, 2)} kg CO₂e", ln=True)
    pdf.cell(0, 10, f"Referencia recomendada: {BENCHMARK} kg CO₂e", ln=True)

    # Guardar en un buffer para descargar
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    return pdf_buffer

st.subheader("📥 Descargar informe")
if st.button("Descargar PDF"):
    pdf_file = generar_pdf()
    st.download_button(
        label="Descargar PDF",
        data=pdf_file,
        file_name="informe_ecoimpact.pdf",
        mime="application/pdf"
    )
