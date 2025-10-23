import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Calculadora de Impacto Ambiental 🌱")

# Ejemplo de datos
detalle = {
    "Energía": 279.6,
    "Combustible": 536.0,
    "Residuos": 285.0,
    "Transporte": 60.0
}
total_emisiones = sum(detalle.values())

# ------------------------------
# Mostrar resultados con recuadros de color
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

# Resultado total destacado
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
# Gráfica futurista sin fondo
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
ax.set_ylabel("kg CO2e", color="#00ffcc")
ax.set_title("Emisiones por categoría", color="#00ffcc")
ax.tick_params(axis='x', colors="#00ffcc")
ax.tick_params(axis='y', colors="#00ffcc")
st.pyplot(fig, use_container_width=True)
