import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load dataset (ganti dengan path dataset yang sesuai)
df = pd.read_csv("/mnt/data/file-Y6tBDfbPXkeazhEJYGhGND")

# Pastikan dataset memiliki kolom yang sesuai
st.title("Dashboard Penjualan Kategori Produk")

# **Grafik 1: Tren Kategori dengan Penjualan Tertinggi per Tahun**
# Menghitung jumlah penjualan per kategori per tahun
data_per_tahun = df.groupby(['year', 'category'])['sales'].sum().reset_index()
max_per_year = data_per_tahun.loc[data_per_tahun.groupby("year")['sales'].idxmax()]

# Plot
fig, ax = plt.subplots()
colors = ['green', 'blue', 'red']  # Warna untuk tiap tahun
for i, row in enumerate(max_per_year.iterrows()):
    row = row[1]
    ax.bar(row['year'], row['sales'], color=colors[i], label=row['category'])
    ax.text(row['year'], row['sales'], str(row['sales']), ha='center', fontsize=12, fontweight='bold')

ax.set_xlabel("Tahun")
ax.set_ylabel("Jumlah Terjual")
ax.set_title("Tren Kategori dengan Penjualan Tertinggi per Tahun")
ax.set_xticks(max_per_year['year'])
ax.set_xticklabels(max_per_year['category'], rotation=20, fontsize=10, fontweight='bold')

st.pyplot(fig)

# **Grafik 2: 5 Kategori dengan Penjualan Tertinggi**
kategori_teratas = df.groupby('category')['sales'].sum().nlargest(5).reset_index()

fig2, ax2 = plt.subplots()
ax2.bar(kategori_teratas['category'], kategori_teratas['sales'], color=['green'] + ['blue']*4)
ax2.set_xlabel("Kategori")
ax2.set_ylabel("Jumlah Terjual")
ax2.set_title("5 Kategori dengan Penjualan Tertinggi")
ax2.set_xticklabels(kategori_teratas['category'], rotation=20, fontsize=10, fontweight='bold')

st.pyplot(fig2)
