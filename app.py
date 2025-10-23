import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="EcoImpact AI", layout="wide", page_icon="🌱")

# -------------------------
# Título de la app
# -------------------------
st.title("EcoImpact AI 🌱")
st.markdown("Calcula el impacto ambiental de tu empresa fácilmente")

# -------------------------
# Banner de Google AdSense arriba
# -------------------------
ad_html_top = """
<!-- Google AdSense -->
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1003274537231191"
     crossorigin="anonymous"></script>
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-1003274537231191"
     data-ad-slot="1234567890"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>
     (adsbygoogle = window.adsbygoogle || []).push({});
</script>
"""
components.html(ad_html_top, height=100)

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
# Reducción por porcentaje
# -------------------------
st.subheader("Reducción por categoría (%)")
col1, col2 = st.columns(2)
with col1:
    energia_red = st.slider("Energía", 0, 100, 0)
    combustible_red = st.slider("Combustible", 0, 100, 0)
with col2:
    residuos_red = st.slider("Residuos", 0, 100, 0)
    transporte_red = st.slider("Transporte", 0, 100, 0)

# -------------------------
# Factores de emisión
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
        "Energía": energia * FE_ENERGIA,
        "Combustible": combustible * FE_COMBUSTIBLE,
        "Residuos": residuos * FE_RESIDUOS,
        "Transporte": transporte * FE_TRANSPORTE
    }

    reducciones = {
        "Energía": emisiones["Energía"] * energia_red / 100,
        "Combustible": emisiones["Combustible"] * combustible_red / 100,
        "Residuos": emisiones["Residuos"] * residuos_red / 100,
        "Transporte": emisiones["Transporte"] * transporte_red / 100
    }

    emisiones_finales = {cat: emisiones[cat] - reducciones[cat] for cat in emisiones}
    total_actual = sum(emisiones.values())
    total_final = sum(emisiones_finales.values())

    # -------------------------
    # Recuadro de totales
    # -------------------------
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
        padding:15px;
        border-radius:12px;
        text-align:center;
        color:white;
        font-size:20px;
        font-weight:bold;">
        🌍 Total emisiones actuales: {total_actual:.2f} kg CO₂e<br>
        💡 Total emisiones tras reducción: {total_final:.2f} kg CO₂e
    </div>
    """, unsafe_allow_html=True)

    # -------------------------
    # Barras de porcentaje de colores
    # -------------------------
    st.subheader("Detalle por categoría")
    colores = {"Energía":"#4caf50", "Combustible":"#ff9800", "Residuos":"#2196f3", "Transporte":"#f44336"}

    for cat in emisiones:
        porcentaje = int((emisiones_finales[cat]/emisiones[cat])*100) if emisiones[cat] != 0 else 0
        st.markdown(f"**{cat}**: {emisiones_finales[cat]:.2f} kg CO₂e ({porcentaje}% del original)")
        st.progress(porcentaje)

# -------------------------
# Banner de Google AdSense abajo
# -------------------------
ad_html_bottom = ad_html_top  # Puedes cambiar slot si quieres otro anuncio
st.markdown("---")
components.html(ad_html_bottom, height=100)
