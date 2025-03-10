import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---- Setup Streamlit ----
st.title("📊 Dashboard Penjualan E-Commerce")
st.write("Analisis data penjualan berdasarkan kategori produk.")

# ---- Load Data ----
@st.cache_data
def load_data():
    orders_df = pd.read_csv("/mnt/data/orders_cleaned.csv")
    review_df = pd.read_csv("/mnt/data/review_cleaned.csv")
    item_df = pd.read_csv("/mnt/data/item_cleaned.csv")
    produk_df = pd.read_csv("/mnt/data/produk_cleaned.csv")
    return orders_df, review_df, item_df, produk_df

orders_df, review_df, item_df, produk_df = load_data()

# ---- Transformasi Data ----
sales_per_category = item_df.groupby("product_category_name")["order_id"].count().sort_values(ascending=False)

# ---- Visualisasi Data ----
st.subheader("🔹 Produk Kategori dengan Total Penjualan Tertinggi")
st.bar_chart(sales_per_category)

st.write("Kategori dengan total penjualan tertinggi berdasarkan data yang sudah dibersihkan.")

# ---- Tren Penjualan Per Tahun ----
st.subheader("🔹 Tren Penjualan Tiap Tahun")
orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"])
orders_df["year"] = orders_df["order_purchase_timestamp"].dt.year
sales_per_year = orders_df.groupby("year")["order_id"].count()

fig, ax = plt.subplots()
ax.plot(sales_per_year.index, sales_per_year.values, marker="o", linestyle="-")
plt.xlabel("Tahun")
plt.ylabel("Jumlah Penjualan")
plt.title("Tren Penjualan Per Tahun")
st.pyplot(fig)

st.write("📌 Dari grafik di atas, kita bisa melihat perkembangan tren penjualan setiap tahun.")
