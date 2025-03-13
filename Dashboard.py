import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale

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
st.sidebar.header("🔧 Filters")
start_date = st.sidebar.date_input("📅 Start Date", df['order_purchase_timestamp'].min())
end_date = st.sidebar.date_input("📅 End Date", df['order_purchase_timestamp'].max())
selected_years = st.sidebar.multiselect("📆 Select Years", df['order_purchase_timestamp'].dt.year.unique(), default=df['order_purchase_timestamp'].dt.year.unique())

# Improved Product Category Filter with Searchable Multi-Select & Scrollable Panel
with st.sidebar.expander("📦 Select Product Categories"):
    all_categories = sorted(df['product_category_name'].dropna().unique())
    select_all = st.checkbox("Select All", value=True)
    
    if select_all:
        category_filter = st.multiselect("📋 Categories", options=all_categories, default=all_categories)
    else:
        category_filter = st.multiselect("📋 Categories", options=all_categories, default=[])

# Apply filters
df_filtered = df[(df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) & 
                 (df['order_purchase_timestamp'] <= pd.Timestamp(end_date)) & 
                 (df['order_purchase_timestamp'].dt.year.isin(selected_years)) & 
                 (df['product_category_name'].isin(category_filter))].copy()

# Main Dashboard Title
st.title("📊 Brazilian E-Commerce Public Dashboard")
st.write("🚀 This dashboard helps analyze sales trends and product performance based on the selected filters.")

# Membagi halaman menjadi dua tabs
tab1, tab2 = st.tabs(["📈 Sales Analysis", "🏆 Best Products"])

with tab1:
    # KPI Metrics
    st.subheader("🏅 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", df_filtered['order_id'].nunique())
    col2.metric("💵 Total Revenue", locale.currency(df_filtered['price'].sum(), grouping=True))
    col3.metric("👤 Unique Customers", df_filtered['customer_id'].nunique())
    
    # Sales Trend over time (Per Tahun)
    st.subheader("📈 Sales Trend Over Time (Yearly)")
    df_filtered['Year'] = df_filtered['order_purchase_timestamp'].dt.year
    sales_trend = df_filtered.groupby('Year')['price'].sum().reset_index()
    
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette("husl", len(sales_trend))
    sns.barplot(data=sales_trend, x='Year', y='price', ax=ax, palette=colors)
    ax.set_title("Tren Penjualan per Tahun", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Total Penjualan ($)", fontsize=12)
    
    for i, row in sales_trend.iterrows():
        ax.text(i, row['price'] * 1.02, f"{row['price']:,.0f}", 
                ha='center', fontsize=10, color='black', fontweight='bold')
    
    st.pyplot(fig)
    st.write(f"💡 The chart above shows the sales trend from {start_date} to {end_date}. You can see how total sales changed by year based on the products you selected. The year with the highest sales may indicate a successful period for the business.")

with tab2:
    # Top Product Categories
    st.subheader("🏆 Top Selling Product Categories")

    top_categories = df_filtered.groupby('product_category_name')['price'].sum().nlargest(10).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("coolwarm", len(top_categories))
    sns.barplot(data=top_categories, x='price', y='product_category_name', ax=ax, palette=colors)
    ax.set_title("Kategori Produk Terlaris", fontsize=14, fontweight='bold')
    ax.set_xlabel("Total Penjualan ($)", fontsize=12)
    ax.set_ylabel("Kategori Produk", fontsize=12)
    
    for p in ax.patches:
        width = p.get_width()
        ax.text(width + max(top_categories['price']) * 0.05, p.get_y() + p.get_height()/1, f'{width:,.0f}', ha='left', fontsize=10, color='black', fontweight='bold')
    
    st.pyplot(fig)
    st.write(f"📌The categories above represent the products with the highest sales based on the filters you selected from {start_date} to {end_date}. If you want to view other categories, please adjust the product filters in the left panel. You can identify the most profitable categories and consider further marketing strategies to boost sales.")
    
    # Top Selling Products
    st.subheader("🔥 Top 5 Best-Selling Products")
    st.write("🚀Here are the top 5 best-selling products based on total sales recorded during the period you selected. Knowing these products is very useful for planning marketing strategies, managing inventory, or gaining better insights into consumer preferences.")
    top_products = df_filtered.groupby(['product_id', 'product_category_name'])[['price']].sum().reset_index()
    top_products = top_products.sort_values(by='price', ascending=False).drop_duplicates(subset=['product_category_name']).head(5)
    
    # Tambahkan nomor urut
    top_products.reset_index(drop=True, inplace=True)
    top_products.index += 1  # Mulai dari 1
    top_products.rename_axis("No", inplace=True)
    
    # Format harga ke mata uang
    top_products['price'] = top_products['price'].apply(lambda x: locale.currency(x, grouping=True))
    
    # Rename column untuk tampilan yang lebih jelas
    top_products.rename(columns={'product_category_name': 'Product Category', 'product_id': 'Product ID'}, inplace=True)
    
    st.write(top_products[['Product ID', 'Product Category','price']])
