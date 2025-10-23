import streamlit as st
import pandas as pd
from fpdf import FPDF
import random

st.set_page_config(page_title="EcoImpact AI", layout="wide")

# -------------------------
# Título y descripción
# -------------------------
st.title("EcoImpact AI 🌱")
st.markdown("Calcula el impacto ambiental de tu empresa fácilmente")

# -------------------------
# Anuncios rotativos
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
    energia = st.number_input("Consumo de energia (kWh)", min_value=0.0, value=0.0, step=10.0)
    combustible = st.number_input("Combustible usado (litros)", min_value=0.0, value=0.0, step=10.0)

with col2:
    residuos = st.number_input("Residuos generados (kg)", min_value=0.0, value=0.0, step=1.0)
    transporte = st.number_input("Transporte recorrido (km)", min_value=0.0, value=0.0, step=5.0)

# -------------------------
# Factores de emision
# -------------------------
FE_ENERGIA = 0.233
FE_COMBUSTIBLE = 2.68
FE_RESIDUOS = 1.9
FE_TRANSPORTE = 0.12

# -------------------------
# Cálculo
# -------------------------
if st.button("Calcular impacto"):
    emisiones = {
        "Energia": energia * FE_ENERGIA,
        "Combustible": combustible * FE_COMBUSTIBLE,
        "Residuos": residuos * FE_RESIDUOS,
        "Transporte": transporte * FE_TRANSPORTE
    }
    total_actual = sum(emisiones.values())

    st.markdown(f"<div style='background-color:#4CAF50;padding:12px;border-radius:8px;color:white;text-align:center;'>"
                f"<b>Emisiones totales: {total_actual:.2f} kg CO2e</b></div>", unsafe_allow_html=True)

    # -------------------------
    # Barras de porcentaje de reduccion
    # -------------------------
    st.subheader("Reducción por porcentaje")
    reduccion = st.slider("Porcentaje de reduccion por categoria (%)", 0, 100, 10)

    emisiones_finales = {cat: val*(1-reduccion/100) for cat, val in emisiones.items()}
    total_final = sum(emisiones_finales.values())

    for cat in emisiones:
        pct = int((emisiones_finales[cat]/emisiones[cat]*100)) if emisiones[cat]!=0 else 0
        st.progress(pct)
        st.write(f"{cat}: {emisiones_finales[cat]:.2f} kg CO2e ({pct}%)")

    st.markdown(f"<div style='background-color:#2196F3;padding:12px;border-radius:8px;color:white;text-align:center;'>"
                f"<b>Total tras reduccion: {total_final:.2f} kg CO2e</b></div>", unsafe_allow_html=True)

    # -------------------------
    # Boton PDF
    # -------------------------
    def generar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "EcoImpact AI - Reporte de Emisiones", ln=True, align="C")
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        for cat in emisiones:
            porcentaje = int((emisiones_finales[cat]/emisiones[cat])*100) if emisiones[cat]!=0 else 0
            pdf.cell(0, 8, f"{cat}: {emisiones_finales[cat]:.2f} kg CO2e ({porcentaje}%)", ln=True)
        pdf.ln(5)
        pdf.cell(0, 8, f"Total emisiones actuales: {total_actual:.2f} kg CO2e", ln=True)
        pdf.cell(0, 8, f"Total emisiones tras reduccion: {total_final:.2f} kg CO2e", ln=True)
        return pdf.output(dest="S").encode("latin-1")

    pdf_file = generar_pdf()
    st.download_button(
        label="📄 Descargar PDF",
        data=pdf_file,
        file_name="reporte_emisiones.pdf",
        mime="application/pdf"
    )

# -------------------------
# Segundo banner abajo
# -------------------------
ad2 = random.choice(banners)
st.markdown("---")
st.image(ad2["img"], use_column_width=True)
st.markdown(f"[Visitar anunciante]({ad2['link']})")
