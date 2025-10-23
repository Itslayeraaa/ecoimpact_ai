import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# --- Configuración de la página ---
st.set_page_config(page_title="EcoImpact AI", layout="wide")

# --- CSS para texto y inputs en blanco y fondo oscuro ---
st.markdown(
    """
    <style>
    body { background-color: #121212; color: white; }
    .stTextInput>div>div>input { color: white; background-color: #1e1e1e; }
    .stNumberInput>div>div>input { color: white; background-color: #1e1e1e; }
    .stButton>button { color: white; background-color: #2e7d32; }
    .stDataFrame { color: white; background-color: #1e1e1e; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Calculadora de Impacto Ambiental 🌱")
st.markdown("Introduce los datos de tu empresa para calcular la huella de carbono.")

# --- Inputs ---
col1, col2 = st.columns(2)

with col1:
    energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, step=1.0)
    combustible = st.number_input("Combustible (litros)", min_value=0.0, step=1.0)

with col2:
    residuos = st.number_input("Residuos generados (kg)", min_value=0.0, step=1.0)
    transporte = st.number_input("Transporte (km)", min_value=0.0, step=1.0)

# --- Factores de emisión simplificados ---
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

# --- Cálculo de emisiones ---
detalle = {
    "Energía": energia * FE_ENERGIA,
    "Combustible": combustible * FE_COMBUSTIBLE,
    "Residuos": residuos * FE_RESIDUOS,
    "Transporte": transporte * FE_TRANSPORTE
}
total_emisiones = sum(detalle.values())

# --- Mostrar resultados ---
st.subheader("📊 Emisiones estimadas (kg CO₂e)")
st.markdown(f"<h2 style='color:white'>{total_emisiones:.2f} kg CO₂e</h2>", unsafe_allow_html=True)

df = pd.DataFrame(list(detalle.items()), columns=["Categoría", "Emisiones (kg CO₂e)"])
st.dataframe(df.style.format("{:.2f}").background_gradient(subset=["Emisiones (kg CO₂e)"], cmap="Greens"))

# --- Gráfica de barras transparente ---
fig, ax = plt.subplots(figsize=(6,4), facecolor="none")
ax.bar(detalle.keys(), detalle.values(), color="#2e7d32", alpha=0.8)
ax.set_facecolor("none")
ax.tick_params(colors='white')
plt.ylabel("kg CO₂e", color="white")
plt.title("Distribución de Emisiones", color="white")
st.pyplot(fig)

# --- Función para generar PDF ---
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(0,0,0)  # texto negro dentro del PDF
    pdf.cell(0, 10, "Informe de Impacto Ambiental", ln=True, align="C")
    pdf.ln(10)

    for cat, val in detalle.items():
        texto = f"{cat}: {val:.2f} kg CO₂e".encode('latin1', 'replace').decode('latin1')
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, texto, ln=True)

    total_text = f"Total de emisiones: {total_emisiones:.2f} kg CO₂e"
    total_text = total_text.encode('latin1', 'replace').decode('latin1')
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, total_text, ln=True)

    return pdf.output(dest='S').encode('latin1')

# --- Botón de descarga PDF ---
st.download_button(
    "📄 Descargar PDF",
    data=generar_pdf(),
    file_name="informe_emisiones.pdf",
    mime="application/pdf"
)
