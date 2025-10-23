import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import random

# ------------------------------
# Anuncios rotativos
# ------------------------------
ads = [
    "https://via.placeholder.com/728x90.png?text=Anuncio+1",
    "https://via.placeholder.com/728x90.png?text=Anuncio+2",
    "https://via.placeholder.com/728x90.png?text=Anuncio+3"
]
st.image(random.choice(ads), use_column_width=True)

st.title("Calculadora de Impacto Ambiental 🌱")
st.write("Calcula tus emisiones de CO₂ de forma sencilla.")

# ------------------------------
# Inputs centrados
# ------------------------------
col1, col2 = st.columns(2)

with col1:
    energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, step=10.0, format="%.2f")
    combustible = st.number_input("Combustible (litros)", min_value=0.0, step=10.0, format="%.2f")

with col2:
    residuos = st.number_input("Residuos (kg)", min_value=0.0, step=1.0, format="%.2f")
    transporte = st.number_input("Transporte (km)", min_value=0.0, step=1.0, format="%.2f")

# ------------------------------
# Factores de emisión
# ------------------------------
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

# ------------------------------
# Cálculo de emisiones
# ------------------------------
total_emisiones = (
    energia * FE_ENERGIA +
    combustible * FE_COMBUSTIBLE +
    residuos * FE_RESIDUOS +
    transporte * FE_TRANSPORTE
)

detalle = {
    "Energía": energia * FE_ENERGIA,
    "Combustible": combustible * FE_COMBUSTIBLE,
    "Residuos": residuos * FE_RESIDUOS,
    "Transporte": transporte * FE_TRANSPORTE
}

df = pd.DataFrame({
    "Categoría": list(detalle.keys()),
    "Emisiones (kg CO2e)": list(detalle.values())
})

# ------------------------------
# Resultados destacados con contraste
# ------------------------------
st.subheader("Resultados Totales")
st.markdown(
    f"<h2 style='color:#00ffcc; background-color:#1f1f1f; padding:10px; border-radius:8px;'>"
    f"{total_emisiones:.2f} kg CO₂e</h2>",
    unsafe_allow_html=True
)

st.dataframe(df.style.background_gradient(subset=["Emisiones (kg CO2e)"], cmap="Greens"))

# ------------------------------
# Gráfica futurista sin fondo
# ------------------------------
fig, ax = plt.subplots(figsize=(6,4), dpi=100)
fig.patch.set_alpha(0)  # fondo transparente
ax.set_facecolor("none")
ax.bar(df["Categoría"], df["Emisiones (kg CO2e)"], color=["#00ffcc","#ff6f61","#ffde59","#7f7fff"], edgecolor='black', linewidth=1.5)
ax.set_ylabel("kg CO2e", color="#00ffcc")
ax.set_title("Emisiones por categoría", color="#00ffcc")
ax.tick_params(axis='x', colors="#00ffcc")
ax.tick_params(axis='y', colors="#00ffcc")
st.pyplot(fig, use_container_width=True)

# ------------------------------
# Generar PDF
# ------------------------------
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, "Reporte de Emisiones", ln=True)
    pdf.ln(5)
    for cat, val in detalle.items():
        pdf.cell(0, 10, f"{cat}: {val:.2f} kg CO2e", ln=True)
    pdf.cell(0, 10, f"Total: {total_emisiones:.2f} kg CO2e", ln=True)
    return pdf

if st.button("Descargar PDF"):
    pdf = generar_pdf()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    st.download_button("Descargar PDF", data=pdf_bytes, file_name="reporte_emisiones.pdf", mime="application/pdf")
