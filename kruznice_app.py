import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader   # <-- 🔥 tento řádek přidej
from PIL import Image

# ----------------------------
# Nastavení aplikace
# ----------------------------
st.set_page_config(page_title="Body na kružnici", layout="centered")

# ----------------------------
# Informace o autorovi
# ----------------------------
autor_jmeno = "Josef Haša"
autor_email = "277826@vutbr.cz"
datum = datetime.today().strftime('%d.%m.%Y')

with st.expander("ℹ️ O aplikaci a autorovi"):
    st.markdown(f"""
    **Body na kružnici** – školní webová aplikace

    - **Autor**: {autor_jmeno}  
    - **Kontakt**: {autor_email}  
    - **Použité technologie**: Python, Streamlit, Matplotlib, ReportLab  
    - **Datum**: {datum}
    """)

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
# Výpočet a vykreslení
# ----------------------------
if radius > 0 and num_points >= 1:
    angles = np.linspace(0, 2 * np.pi, int(num_points), endpoint=False)
    x_points = x_center + radius * np.cos(angles)
    y_points = y_center + radius * np.sin(angles)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.plot(x_points, y_points, 'o', color=color, label='Body na kružnici')
    if show_lines:
        ax.plot(np.append(x_points, x_points[0]), np.append(y_points, y_points[0]),
                '-', color=color, alpha=0.5, label='Spojení bodů')
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
    # PŘÍPRAVA PDF
    # ----------------------------
    # 1. Uložení obrázku z grafu jako PNG
    img_buf = BytesIO()
    fig.savefig(img_buf, format='png')
    img_buf.seek(0)
    img = Image.open(img_buf)

    # 2. Vytvoření PDF s parametry + grafem
    pdf_buf = BytesIO()
    c = canvas.Canvas(pdf_buf, pagesize=A4)
    width, height = A4

    # Strana 1 – parametry
    c.setFont("Helvetica-Bold", 16)
    c.drawString(2 * cm, height - 2.5 * cm, "Parametry úlohy – Body na kružnici")
    c.setFont("Helvetica", 12)

    c.drawString(2 * cm, height - 4 * cm, f"Střed kružnice: ({x_center}, {y_center}) {unit}")
    c.drawString(2 * cm, height - 5 * cm, f"Poloměr: {radius} {unit}")
    c.drawString(2 * cm, height - 6 * cm, f"Počet bodů: {num_points}")
    c.drawString(2 * cm, height - 7 * cm, f"Barva bodů: {color}")
    c.drawString(2 * cm, height - 8 * cm, f"Spojit body čárou: {'Ano' if show_lines else 'Ne'}")
    c.drawString(2 * cm, height - 9.5 * cm, f"Jednotky os: {unit}")
    c.drawString(2 * cm, height - 11 * cm, f"Autor: {autor_jmeno}")
    c.drawString(2 * cm, height - 12 * cm, f"E-mail: {autor_email}")
    c.drawString(2 * cm, height - 13.5 * cm, f"Datum: {datum}")

    c.showPage()

    # Strana 2 – obrázek grafu
    img_width, img_height = img.size
    max_width = width - 4 * cm
    max_height = height - 4 * cm
    scale = min(max_width / img_width, max_height / img_height)
    new_width = img_width * scale
    new_height = img_height * scale
    img = img.resize((int(new_width), int(new_height)))
    temp_img = BytesIO()
    img.save(temp_img, format="PNG")
    temp_img.seek(0)

    c.drawImage(ImageReader(temp_img), x=2 * cm, y=height - 2 * cm - new_height, width=new_width, height=new_height)
    c.showPage()
    c.save()

    st.download_button(
        label="📄 Stáhnout PDF s parametry a grafem",
        data=pdf_buf.getvalue(),
        file_name=f"kruznice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )
