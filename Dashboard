import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- Setup Streamlit ----
st.title("📊 Dashboard Penjualan E-Commerce")
st.write("Analisis data penjualan berdasarkan kategori produk antara tahun 2016-2018.")

# ---- Data ----
data = {
    "year": [2016, 2017, 2018],
    "Bed Bath Table": [0, 6008, 6470],
    "Health & Beauty": [0, 0, 9670],
    "Sports & Leisure": [0, 0, 8641],
    "Furniture & Decor": [65, 0, 8334],
    "Computers & Accessories": [0, 0, 7827]
}

df = pd.DataFrame(data)

# ---- Pertanyaan 1: Produk kategori dengan total penjualan tertinggi ----
st.subheader("🔹 Produk Kategori dengan Total Penjualan Tertinggi (2016-2018)")
total_sales = df.iloc[:, 1:].sum().sort_values(ascending=False)
st.bar_chart(total_sales)

st.write("Kategori dengan total penjualan tertinggi adalah **Bed Bath Table** dengan **12.718 unit terjual**.")

# ---- Pertanyaan 2: Tren kategori produk dengan penjualan tertinggi per tahun ----
st.subheader("🔹 Tren Penjualan Produk Tertinggi Tiap Tahun")
fig, ax = plt.subplots()
for category in df.columns[1:]:
    ax.plot(df["year"], df[category], marker="o", label=category)

plt.xlabel("Tahun")
plt.ylabel("Jumlah Terjual")
plt.title("Tren Penjualan Berdasarkan Kategori")
plt.legend()
st.pyplot(fig)

st.write("📌 Dari grafik di atas, terlihat bahwa **Bed Bath Table** mengalami peningkatan penjualan dari tahun 2017 ke 2018.")

st.write("💡 **Kesimpulan:**")
st.write("- **Bed Bath Table** menjadi kategori dengan total penjualan tertinggi dalam 3 tahun.")
st.write("- Tahun 2016 masih memiliki penjualan yang sangat rendah.")
st.write("- Penjualan mengalami kenaikan signifikan di tahun 2017 dan 2018.")

