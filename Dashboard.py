import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale
import numpy as np

# Set locale untuk format mata uang
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Caching data untuk mempercepat loading
@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)

# Load cleaned datasets
orders = load_data("orders_cleaned.csv")
order_items = load_data("item_cleaned.csv")
products = load_data("produk_cleaned.csv")

# Merge datasets
df = orders.merge(order_items, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")

# Convert date column to datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", df['order_purchase_timestamp'].max())
selected_years = st.sidebar.multiselect("Select Years", df['order_purchase_timestamp'].dt.year.unique(), default=df['order_purchase_timestamp'].dt.year.unique())
category_filter = st.sidebar.multiselect("Select Product Categories", df['product_category_name'].dropna().unique(), default=df['product_category_name'].dropna().unique())

# Apply filters
df_filtered = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                 (df['order_purchase_timestamp'] <= pd.Timestamp(end_date)) & 
                 (df['order_purchase_timestamp'].dt.year.isin(selected_years)) & 
                 (df['product_category_name'].isin(category_filter))].copy()

# Main Dashboard Title
st.title("📊 E-Commerce Sales Dashboard")
st.write("🚀 Dashboard ini membantu menganalisis tren penjualan dan performa produk.")

# KPI Metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", locale.currency(df_filtered['price'].sum(), grouping=True))
col3.metric("Unique Customers", df_filtered['customer_id'].nunique())

# Sales Trend over time (Per Tahun)
st.subheader("Sales Trend Over Time (Yearly)")
df_filtered['Year'] = df_filtered['order_purchase_timestamp'].dt.year
sales_trend = df_filtered.groupby('Year')['price'].sum().reset_index()

sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))
colors = sns.color_palette("husl", len(sales_trend))  # Warna berbeda untuk setiap batang
sns.barplot(data=sales_trend, x='Year', y='price', ax=ax, palette=colors)
ax.set_title("Tren Penjualan per Tahun", fontsize=12, fontweight='bold')
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Total Penjualan ($)", fontsize=12)

# Tambahkan label angka ke setiap batang data, lebih dekat ke batang
for i, row in sales_trend.iterrows():
    ax.text(i, row['price'] * 1.02, f"{row['price']:,.0f}", 
            ha='center', fontsize=10, color='black', fontweight='bold')



st.pyplot(fig)
st.write("💡 Grafik di atas menunjukkan perkembangan total penjualan dari waktu ke waktu.")

# Top Product Categories
st.subheader("Top Selling Product Categories")
top_categories = df_filtered.groupby('product_category_name')['price'].sum().nlargest(10).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
colors = sns.color_palette("coolwarm", len(top_categories))  # Warna berbeda untuk setiap batang
sns.barplot(data=top_categories, x='price', y='product_category_name', ax=ax, palette=colors)
ax.set_title("Kategori Produk Terlaris", fontsize=14, fontweight='bold')
ax.set_xlabel("Total Penjualan ($)", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)

# Tambahkan label angka dengan jarak yang cukup dari batang
for p in ax.patches:
    width = p.get_width()
    ax.text(width + max(top_categories['price']) * 0.05, p.get_y() + p.get_height()/1, f'{width:,.0f}', ha='left', fontsize=10, color='black', fontweight='bold')

st.pyplot(fig)
st.write("📌 Kategori di atas merupakan produk dengan penjualan tertinggi.")

st.write("💡 Dashboard by Streamlit | 🛠 Built with ❤")
