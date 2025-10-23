import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from io import BytesIO

# ------------------------------
# Estilos CSS
# ------------------------------
st.markdown(
    """
    <style>
    /* Fondo de inputs y estilo */
    div.stNumberInput > div > input {
        background-color: #2b2b2b;
        color: #00ffcc;
        border: 2px solid #00ffcc;
        border-radius: 8px;
        padding: 5px 10px;
    }
    div.stNumberInput > label {
        color: #00ffcc;
        font-weight: bold;
    }

    /* Fondo de toda la app */
    .stApp {
        background-color: #0a0a0a;
        color: #ffffff;
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.title("Calculadora de Impacto Ambiental 🌱", anchor=None)

# ------------------------------
# Inputs centrados
# ------------------------------
col1, col2 = st.columns(2)
with col1:
    energia = st.number_input("Consumo de energía (kWh)", min_value=0.0)
    combustible = st.number_input("Combustible (litros)", min_value=0.0)
with col2:
    residuos = st.number_input("Residuos (kg)", min_value=0.0)
    transporte = st.number_input("Transporte (km)", min_value=0.0)

# ------------------------------
# Cálculos de emisiones
# ------------------------------
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

detalle = {
    "Energía": energia * FE_ENERGIA,
    "Combustible": combustible * FE_COMBUSTIBLE,
    "Residuos": residuos * FE_RESIDUOS,
    "Transporte": transporte * FE_TRANSPORTE
}
total_emisiones = sum(detalle.values())

# ------------------------------
# Mostrar resultados por categoría
# ------------------------------
st.subheader("Resultados por categoría")
for cat, val in detalle.items():
    st.markdown(
        f"""
        <div style="
            background-color: #1f1f1f;
            color: #00ffcc;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        ">
            {cat}: {val:.2f} kg CO₂e
        </div>
        """,
        unsafe_allow_html=True
    )

# Total destacado
st.subheader("Total de emisiones")
st.markdown(
    f"""
    <div style="
        background-color: #0a0a0a;
        color: #ff6f61;
        padding: 15px;
        border-radius: 12px;
        font-size: 24px;
        font-weight: bold;
        text-align:center;
    ">
        {total_emisiones:.2f} kg CO₂e
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Gráfica futurista
# ------------------------------
df = pd.DataFrame({
    "Categoría": list(detalle.keys()),
    "Emisiones (kg CO2e)": list(detalle.values())
})

fig, ax = plt.subplots(figsize=(6,4), dpi=100)
fig.patch.set_alpha(0)  # Fondo transparente
ax.set_facecolor("none")
ax.bar(df["Categoría"], df["Emisiones (kg CO2e)"], 
       color=["#00ffcc","#ff6f61","#ffde59","#7f7fff"], 
       edgecolor='black', linewidth=1.5)
ax.set_ylabel("kg CO₂e", color="#00ffcc")
ax.set_title("Emisiones por categoría", color="#00ffcc")
ax.tick_params(axis='x', colors="#00ffcc")
ax.tick_params(axis='y', colors="#00ffcc")
st.pyplot(fig, use_container_width=True)

# ------------------------------
# Descargar PDF
# ------------------------------
def generar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe de Impacto Ambiental", ln=True, align="C")
    pdf.ln(10)
    
    for cat, val in detalle.items():
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"{cat}: {val:.2f} kg CO₂e", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Total de emisiones: {total_emisiones:.2f} kg CO₂e", ln=True)
    
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

st.download_button(
    "📄 Descargar PDF",
    data=generar_pdf(),
    file_name="informe_emisiones.pdf",
    mime="application/pdf"
)
