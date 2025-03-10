import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned datasets
orders = pd.read_csv("/mnt/data/orders_cleaned.csv")
order_items = pd.read_csv("/mnt/data/item_cleaned.csv")
products = pd.read_csv("/mnt/data/produk_cleaned.csv")

# Merge datasets
df = orders.merge(order_items, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")

# Convert date column to datetime
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

# Sidebar filters
st.sidebar.header("Filters")
start_date = st.sidebar.date_input("Start Date", df['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("End Date", df['order_purchase_timestamp'].max())
category_filter = st.sidebar.multiselect("Select Product Categories", df['product_category_name'].unique(), default=df['product_category_name'].unique())

# Apply filters
df_filtered = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                 (df['order_purchase_timestamp'] <= pd.Timestamp(end_date)) & 
                 (df['product_category_name'].isin(category_filter))]

# Main Dashboard Title
st.title("E-Commerce Sales Dashboard")
st.markdown("""Dashboard ini menampilkan analisis penjualan dari data e-commerce, termasuk metrik utama, tren penjualan, dan kategori produk teratas.""")

# KPI Metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Orders", df_filtered['order_id'].nunique())
col2.metric("Total Revenue", f"$ {df_filtered['price'].sum():,.2f}")
col3.metric("Unique Customers", df_filtered['customer_id'].nunique())

# Sales Trend over time
st.subheader("Sales Trend Over Time")
df_filtered['Year-Month'] = df_filtered['order_purchase_timestamp'].dt.to_period('M').astype(str)
sales_trend = df_filtered.groupby('Year-Month')['price'].sum().reset_index()
sales_trend['Year-Month'] = sales_trend['Year-Month'].astype(str)

sns.set_style("darkgrid")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=sales_trend, x='Year-Month', y='price', ax=ax, marker='o', color='royalblue')
ax.set_title("Tren Penjualan per Bulan", fontsize=14, fontweight='bold')
ax.set_xlabel("Bulan", fontsize=12)
ax.set_ylabel("Total Penjualan ($)", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)
st.markdown("""Grafik di atas menunjukkan perkembangan total penjualan dari waktu ke waktu. Lonjakan tertentu mungkin mengindikasikan periode promosi atau peningkatan permintaan musiman.""")

# Top Product Categories
st.subheader("Top Selling Product Categories")
top_categories = df_filtered.groupby('product_category_name')['price'].sum().nlargest(10).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_categories, x='price', y='product_category_name', ax=ax, palette='viridis')
ax.set_title("Kategori Produk Terlaris", fontsize=14, fontweight='bold')
ax.set_xlabel("Total Penjualan ($)", fontsize=12)
ax.set_ylabel("Kategori Produk", fontsize=12)
st.pyplot(fig)
st.markdown("""Kategori di atas merupakan produk dengan penjualan tertinggi. Hal ini bisa menjadi wawasan bagi pemilik bisnis untuk memahami tren pasar.""")

