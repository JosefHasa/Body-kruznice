import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Body na kružnici", layout="centered")

st.title("🎯 Body na kružnici")

# Uživatelské vstupy
x_center = st.number_input("Zadej X souřadnici středu kružnice:", value=0.0)
y_center = st.number_input("Zadej Y souřadnici středu kružnice:", value=0.0)
radius = st.number_input("Zadej poloměr kružnice:", min_value=0.0, value=5.0)
num_points = st.number_input("Zadej počet bodů na kružnici:", min_value=1, value=12, step=1)
color = st.color_picker("Vyber barvu bodů:", "#ff0000")

# Výpočet bodů
if radius > 0 and num_points >= 1:
    angles = np.linspace(0, 2 * np.pi, int(num_points), endpoint=False)
    x_points = x_center + radius * np.cos(angles)
    y_points = y_center + radius * np.sin(angles)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.plot(x_points, y_points, 'o', color=color, label='Body na kružnici')
    ax.plot(x_center, y_center, 'x', color='black', label='Střed')
    ax.set_title("Body rovnoměrně rozmístěné na kružnici")
    ax.legend()
    ax.grid(True)

    padding = radius * 1.2
    ax.set_xlim(x_center - padding, x_center + padding)
    ax.set_ylim(y_center - padding, y_center + padding)

    st.pyplot(fig)
