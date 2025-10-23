import streamlit as st
import random

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
# Cálculo
# -------------------------
if st.button("Calcular impacto"):
    emisiones_energia = energia * FE_ENERGIA
    emisiones_combustible = combustible * FE_COMBUSTIBLE
    emisiones_residuos = residuos * FE_RESIDUOS
    emisiones_transporte = transporte * FE_TRANSPORTE

    total_emisiones = emisiones_energia + emisiones_combustible + emisiones_residuos + emisiones_transporte

    st.success(f"🌍 Emisiones totales: **{total_emisiones:.2f} kg CO₂e**")

    # Mostrar detalle en columnas
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Energía (kg CO₂e)", f"{emisiones_energia:.2f}")
        st.metric("Combustible (kg CO₂e)", f"{emisiones_combustible:.2f}")
    with col2:
        st.metric("Residuos (kg CO₂e)", f"{emisiones_residuos:.2f}")
        st.metric("Transporte (kg CO₂e)", f"{emisiones_transporte:.2f}")

# -------------------------
# Segundo banner abajo
# -------------------------
ad2 = random.choice(banners)
st.markdown("---")
st.image(ad2["img"], use_column_width=True)
st.markdown(f"[Visitar anunciante]({ad2['link']})")

# -------------------------
# Pop-up tipo oferta
# -------------------------
with st.expander("🎁 Oferta especial: accede al plan Premium sin anuncios"):
    st.image("https://via.placeholder.com/728x90.png?text=Oferta+Premium", use_column_width=True)
    st.markdown("[Paga aquí para desbloquear Premium](https://example.com/premium)")
