import streamlit as st
import pandas as pd
import altair as alt
from io import BytesIO
from fpdf import FPDF

# ===== Configuración página =====
st.set_page_config(page_title="🌿 EcoImpact AI Futuristic", layout="wide")
st.markdown("""
<h1 style='text-align:center; color:#00FFAA; font-family:Courier; text-shadow: 2px 2px 10px #000;'>🌿 EcoImpact AI</h1>
<h3 style='text-align:center; color:#66FFCC; font-family:Courier;'>Calculadora de Impacto Ambiental Premium Futurista</h3>
""", unsafe_allow_html=True)

# ===== Estado de suscripción =====
if "plan" not in st.session_state:
    st.session_state.plan = "Básica"

# ===== Función de cálculo =====
def calcular_emisiones(energia, combustible, residuos, transporte):
    FE_ENERGIA = 0.233
    FE_COMBUSTIBLE = 2.68
    FE_RESIDUOS = 1.9
    FE_TRANSPORTE = 0.12
    detalle = {
        "Categoría": ["Energía", "Combustible", "Residuos", "Transporte"],
        "Emisiones (kg CO₂e)": [
            energia * FE_ENERGIA,
            combustible * FE_COMBUSTIBLE,
            residuos * FE_RESIDUOS,
            transporte * FE_TRANSPORTE
        ]
    }
    df = pd.DataFrame(detalle)
    total = df["Emisiones (kg CO₂e)"].sum()
    return total, df

# ===== Función para PDF =====
def generar_pdf(df, total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Informe de Impacto Ambiental", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    for i, row in df.iterrows():
        pdf.cell(0, 10, f"{row['Categoría']}: {row['Emisiones (kg CO₂e)']:.2f} kg CO₂e", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Emisiones Totales: {total:.2f} kg CO₂e", ln=True)
    buffer = BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

# ===== Estilos futuristas =====
card_style = """
<div style='background: linear-gradient(135deg, #0ff, #6f6); padding:20px; border-radius:20px; box-shadow: 0px 0px 20px #00ffcc; margin:10px;'>
<h3 style='color:#000; font-weight:bold;'>PLAN</h3>
{features}
</div>
"""

button_style = """
<button style='background-color:#00ffcc; color:#000; padding:10px 20px; border:none; border-radius:10px; font-weight:bold; font-size:16px; cursor:pointer; box-shadow: 0px 0px 10px #0ff;'>
{label}
</button>
"""

# ===== Pestañas =====
tab1, tab2, tab3 = st.tabs(["Básica", "Premium", "Elite"])

# ---------------- BÁSICA ----------------
with tab1:
    st.markdown("<h2 style='color:#00FFAA;'>🌱 Básica (Gratis)</h2>", unsafe_allow_html=True)
    st.markdown(card_style.format(features="""
    <ul>
    <li>✅ Calculo básico de emisiones</li>
    <li>⚠️ Con anuncios</li>
    <li>📊 Gráficas limitadas</li>
    </ul>
    """), unsafe_allow_html=True)

    energia = st.number_input("Consumo de energía (kWh)", min_value=0.0, key="e_b")
    combustible = st.number_input("Combustible (litros)", min_value=0.0, key="c_b")
    residuos = st.number_input("Residuos (kg)", min_value=0.0, key="r_b")
    transporte = st.number_input("Transporte (km)", min_value=0.0, key="t_b")

    if st.button("Calcular Básica"):
        total, _ = calcular_emisiones(energia, combustible, residuos, transporte)
        st.success(f"Emisiones totales: {total:.2f} kg CO₂e")
        st.warning("Versión gratuita con anuncios.")

# ---------------- PREMIUM ----------------
with tab2:
    st.markdown("<h2 style='color:#66FFCC;'>🌟 Premium</h2>", unsafe_allow_html=True)
    st.markdown(card_style.format(features="""
    <ul>
    <li>✅ Todo Básica</li>
    <li>✅ Gráficas interactivas</li>
    <li>✅ Simulaciones con sliders</li>
    <li>✅ Sin anuncios</li>
    </ul>
    """), unsafe_allow_html=True)

    if st.button("Suscribirme a Premium"):
        st.session_state.plan = "Premium"
        st.success("¡Suscripción Premium activada!")

    if st.session_state.plan == "Premium":
        energia = st.slider("Consumo de energía (kWh)", 0.0, 5000.0, 1000.0)
        combustible = st.slider("Combustible (litros)", 0.0, 1000.0, 100.0)
        residuos = st.slider("Residuos (kg)", 0.0, 500.0, 50.0)
        transporte = st.slider("Transporte (km)", 0.0, 2000.0, 200.0)

        if st.button("Calcular Premium"):
            total, df = calcular_emisiones(energia, combustible, residuos, transporte)
            st.success(f"Emisiones totales: {total:.2f} kg CO₂e")
            chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x='Categoría', y='Emisiones (kg CO₂e)', color='Categoría'
            )
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(df.style.background_gradient(subset=["Emisiones (kg CO₂e)"], cmap="Greens"))

# ---------------- ELITE ----------------
with tab3:
    st.markdown("<h2 style='color:#FFD700;'>🏆 Elite</h2>", unsafe_allow_html=True)
    st.markdown(card_style.format(features="""
    <ul>
    <li>✅ Todo Premium</li>
    <li>✅ Simulaciones avanzadas</li>
    <li>✅ PDF descargable</li>
    <li>✅ Comparativa con benchmarks</li>
    <li>✅ Interfaz futurista completa</li>
    </ul>
    """), unsafe_allow_html=True)

    if st.button("Suscribirme a Elite"):
        st.session_state.plan = "Elite"
        st.success("¡Suscripción Elite activada!")

    if st.session_state.plan == "Elite":
        energia = st.slider("Consumo de energía (kWh)", 0.0, 10000.0, 1500.0)
        combustible = st.slider("Combustible (litros)", 0.0, 2000.0, 200.0)
        residuos = st.slider("Residuos (kg)", 0.0, 1000.0, 100.0)
        transporte = st.slider("Transporte (km)", 0.0, 5000.0, 500.0)

        if st.button("Calcular Elite"):
            total, df = calcular_emisiones(energia, combustible, residuos, transporte)
            st.success(f"Emisiones totales: {total:.2f} kg CO₂e")
            chart = alt.Chart(df).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                x='Categoría', y='Emisiones (kg CO₂e)', color='Categoría'
            )
            st.altair_chart(chart, use_container_width=True)
            st.dataframe(df.style.background_gradient(subset=["Emisiones (kg CO₂e)"], cmap="Greens"))
            pdf_buffer = generar_pdf(df, total)
            st.download_button("📄 Descargar Informe PDF", data=pdf_buffer, file_name="informe_impacto.pdf", mime="application/pdf")
