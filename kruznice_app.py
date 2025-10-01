import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime

# ----------------------------
# Nastavení aplikace
# ----------------------------
st.set_page_config(page_title="Body na kružnici", layout="centered")

# ----------------------------
# Základní informace o autorovi
# ----------------------------
with st.expander("ℹ️ O aplikaci a autorovi"):
    st.markdown("""
    **Body na kružnici**  
    Webová aplikace vytvořená jako školní projekt.

    - **Autor**: Jan Novák  
    - **E-mail**: jan.novak@email.cz  
    - **Použité technologie**: Python, Streamlit, Matplotlib  
    - **Datum**: {date}

    Aplikace vykresluje rovnoměrně rozmístěné body na kružnici podle zadaných parametrů.
    """.format(date=datetime.today().strftime('%d.%m.%Y')))

st.title("🎯 Body na kružnici")

# ----------------------------
# Uživatelské vstupy
# ----------------------------
col1, col2 = st.columns(2)
with col1:
    x_center = st.number_input("X souřadnice středu (m):", value=0.0, format="%.2f")
    radius = st.number_input("Poloměr kružnice (m):", min_value=0.0, value=5.0, format="%.2f")
    color = st.color_picker("Barva bodů:", "#ff0000")
with col2:
    y_center = st.number_input("Y souřadnice středu (m):", value=0.0, format="%.2f")
    num_points = st.number_input("Počet bodů:", min_value=1, value=12, step=1)

show_lines = st.checkbox("Spojit body čárou")
unit = st.selectbox("Jednotka os", ["m", "cm", "mm"], index=0)

# ----------------------------
# Výpočet souřadnic bodů
# ----------------------------
if radius > 0 and num_points >= 1:
    angles = np.linspace(0, 2 * np.pi, int(num_points), endpoint=False)
    x_points = x_center + radius * np.cos(angles)
    y_points = y_center + radius * np.sin(angles)

    # ----------------------------
    # Vykreslení grafu
    # ----------------------------
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Body
    ax.plot(x_points, y_points, 'o', color=color, label='Body na kružnici')

    # Spojovací čára
    if show_lines:
        ax.plot(np.append(x_points, x_points[0]),
                np.append(y_points, y_points[0]),
                '-', color=color, alpha=0.5, label='Spojení bodů')

    # Střed
    ax.plot(x_center, y_center, 'x', color='black', label='Střed')

    ax.set_title("Body na kružnici")
    ax.set_xlabel(f"X [{unit}]")
    ax.set_ylabel(f"Y [{unit}]")
    ax.grid(True)
    ax.legend()

    padding = radius * 1.2
    ax.set_xlim(x_center - padding, x_center + padding)
    ax.set_ylim(y_center - padding, y_center + padding)

    st.pyplot(fig)

    # ----------------------------
    # Tlačítko ke stažení obrázku jako PDF
    # ----------------------------
    buf = BytesIO()
    fig.savefig(buf, format="pdf")
    st.download_button(
        label="📥 Stáhnout jako PDF",
        data=buf.getvalue(),
        file_name=f"kruznice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

    # Parametry úlohy do PDF
    st.markdown("---")
    st.subheader("📄 Parametry úlohy")
    st.markdown(f"""
    - **Střed kružnice**: ({x_center}, {y_center}) {unit}  
    - **Poloměr**: {radius} {unit}  
    - **Počet bodů**: {num_points}  
    - **Barva bodů**: `{color}`  
    - **Spojení čarou**: {"Ano" if show_lines else "Ne"}  
    - **Autor**: Jan Novák  
    - **Datum**: {datetime.today().strftime('%d.%m.%Y')}  
    """)
