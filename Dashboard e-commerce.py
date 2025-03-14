import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from babel.numbers import format_currency  # Ganti locale dengan babel

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
    select_all = st.checkbox("Select All", value=False)
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
    # Sales Trend Over Time (Yearly) with Top Categories
    st.subheader("📈 Sales Trend Over Time (Yearly)")

    df_filtered['Year'] = df_filtered['order_purchase_timestamp'].dt.year

    # Ambil 5 kategori teratas berdasarkan total penjualan
    top_categories = df_filtered.groupby('product_category_name')['price'].sum().nlargest(5).index.tolist()

    # Filter data hanya untuk kategori teratas
    df_top_categories = df_filtered[df_filtered['product_category_name'].isin(top_categories)]

    # Grup berdasarkan tahun dan kategori produk (hanya kategori teratas)
    sales_by_year_top_categories = df_top_categories.groupby(['Year', 'product_category_name'])['price'].sum().reset_index()

    # Buat grafik
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = sns.color_palette("husl", len(top_categories))

    # Plot bar chart
    sns.barplot(data=sales_by_year_top_categories, x='Year', y='price', hue='product_category_name', ax=ax, palette=colors)
    ax.set_title("Tren Penjualan per Tahun dengan Kategori Teratas", fontsize=12, fontweight='bold')
    ax.set_xlabel("Tahun", fontsize=12)
    ax.set_ylabel("Total Penjualan ($)", fontsize=12)

    # Hitung threshold (1% dari total penjualan maksimum)
    if not sales_by_year_top_categories.empty and 'price' in sales_by_year_top_categories.columns:
        threshold = max(sales_by_year_top_categories['price']) * 0.01
    else:
        st.warning("Tidak ada data penjualan yang memenuhi kriteria filter atau kolom 'price' tidak ditemukan.")
        threshold = 0  # Atur threshold ke 0 jika data tidak valid

    # Tambahkan label total penjualan di atas batang grafik
    for p in ax.patches:
        height = p.get_height()
        if height >= threshold:  # Hanya tampilkan label jika total penjualan melebihi threshold
            ax.text(
                p.get_x() + p.get_width() / 2.,  # Posisi horizontal (tengah batang)
                height + max(sales_by_year_top_categories['price']) * 0.01,  # Posisi vertikal (sedikit di atas batang)
                f"${height:,.0f}",  # Teks label
                ha='center',  # Posisi horizontal teks (center)
                fontsize=8,  # Ukuran font lebih kecil
                color='black',  # Warna teks
                fontweight='bold'  # Ketebalan teks
            )

    # Buat legenda kategori di sebelah kanan grafik
    ax.legend(title="Kategori Teratas", loc='center left', bbox_to_anchor=(1, 0.5))

    # Adjust layout agar elemen grafik tidak tumpang tindih
    plt.tight_layout()

    st.pyplot(fig)
    st.write(f"💡 The chart above shows the sales trend from {start_date} to {end_date}, highlighting the top 5 best-selling product categories each year. This insight helps in identifying trends in product demand.")

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
    st.write(f"📌The categories above represent the products with the highest sales based on the filters you selected from {start_date} to {end_date}.")
    
    # Top Selling Products
    st.subheader("🔥 Top 5 Best-Selling Products")
    st.write("🚀Here are the top 5 best-selling products based on total sales recorded during the period you selected.")
    top_products = df_filtered.groupby(['product_id', 'product_category_name'])[['price']].sum().reset_index()
    top_products = top_products.sort_values(by='price', ascending=False).drop_duplicates(subset=['product_category_name']).head(5)
    
    top_products.reset_index(drop=True, inplace=True)
    top_products.index += 1
    top_products.rename_axis("No", inplace=True)
    
    top_products['price'] = top_products['price'].apply(lambda x: format_currency(x, 'USD', locale='en_US'))  # Ganti locale dengan babel
    top_products.rename(columns={'product_category_name': 'Product Category', 'product_id': 'Product ID'}, inplace=True)
    
    st.write(top_products[['Product ID', 'Product Category','price']])
