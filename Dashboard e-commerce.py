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

# Tentukan batas tanggal minimum dan maksimum
min_date = pd.Timestamp('2016-01-01')
max_date = pd.Timestamp('2018-12-31')

# Sidebar filters
st.sidebar.header("🔧 Filters")
start_date = st.sidebar.date_input(
    "📅 Start Date", 
    min_date,  # Default: 1 Januari 2016
    min_value=min_date,  # Batas bawah: 1 Januari 2016
    max_value=max_date   # Batas atas: 31 Desember 2018
)
end_date = st.sidebar.date_input(
    "📅 End Date", 
    max_date,  # Default: 31 Desember 2018
    min_value=min_date,  # Batas bawah: 1 Januari 2016
    max_value=max_date   # Batas atas: 31 Desember 2018
)

# Ambil tahun yang valid (2016, 2017, 2018)
valid_years = [2016, 2017, 2018]

# Filter tahun yang dipilih
selected_years = st.sidebar.multiselect(
    "📆 Select Years", 
    options=valid_years,  # Hanya tampilkan tahun 2016, 2017, 2018
    default=valid_years   # Default: semua tahun (2016, 2017, 2018)
)

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
    # KPI Metrics
    st.subheader("🏅 Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total Orders", df_filtered['order_id'].nunique())

    # Ensure 'price' is numeric and handle NaN values
    df_filtered['price'] = pd.to_numeric(df_filtered['price'], errors='coerce').fillna(0)

    # Total Revenue (menggunakan babel)
    total_revenue = format_currency(df_filtered['price'].sum(), 'USD', locale='en_US')
    col2.metric("💵 Total Revenue", total_revenue)
    
    col3.metric("👤 Unique Customers", df_filtered['customer_id'].nunique())

    # ===================== Kategori dengan Penjualan Tertinggi ===================== #

    # Menghitung jumlah penjualan per kategori dari df_filtered
    if 'product_category_name' in df_filtered.columns:
        count_kategori = df_filtered['product_category_name'].value_counts()
    else:
        raise ValueError("Kolom 'product_category_name' tidak ditemukan dalam dataframe!")

    # Membuat DataFrame untuk kategori paling laris
    kategori_paling_laris = pd.DataFrame({
        'product_category': count_kategori.index[:5],  # Ambil 5 kategori teratas
        'jumlah_terjual': count_kategori.values[:5]
    })

    # Pastikan DataFrame sudah memiliki index yang sesuai
    kategori_paling_laris = kategori_paling_laris.set_index('product_category')

    # Plot bar chart untuk kategori dengan penjualan tertinggi
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(kategori_paling_laris.index, kategori_paling_laris['jumlah_terjual'], color='skyblue')

    # Menyesuaikan tampilan sumbu x
    ax.set_xticks(range(len(kategori_paling_laris.index)))  # Pastikan ada tick untuk setiap kategori
    ax.set_xticklabels(kategori_paling_laris.index, rotation=45, ha='right')

    # Menambahkan judul dan label
    ax.set_title('5 Kategori dengan Penjualan Tertinggi')
    ax.set_ylabel('Jumlah Terjual')

    # Menampilkan grafik
    st.pyplot(fig)

    # ===================== Tren Kategori dengan Penjualan Tertinggi per Tahun ===================== #

    # Hitung tren penjualan tahunan dari df_filtered
    tren_terlaris = df_filtered.groupby([df_filtered['order_purchase_timestamp'].dt.year, 'product_category_name'])[['order_id']].count().reset_index()
    tren_terlaris.rename(columns={'order_id': 'jumlah_terjual', 'product_category_name': 'product_category', 'order_purchase_timestamp': 'year'}, inplace=True)

    # Ambil kategori dengan penjualan tertinggi per tahun
    tren_terlaris = tren_terlaris.loc[tren_terlaris.groupby('year')['jumlah_terjual'].idxmax()]

    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 5))

    # Buat bar chart
    bars = ax.bar(tren_terlaris['year'].astype(int), tren_terlaris['jumlah_terjual'], color=['green', 'blue', 'red'])

    # Tambahkan label jumlah terjual di atas bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 200, f'{int(height)}',
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='black')

    # Tambahkan label kategori di bawah sumbu x
    for i, category in enumerate(tren_terlaris['product_category']):
        ax.text(bars[i].get_x() + bars[i].get_width()/2, -500, category,
                ha='center', va='top', fontsize=10, fontweight='bold', color='black', rotation=30)

    ax.set_xticks(tren_terlaris['year'].astype(int))
    ax.set_xticklabels(tren_terlaris['year'].astype(int))
    ax.set_title('Tren Kategori dengan Penjualan Tertinggi per Tahun')
    ax.set_ylabel('Jumlah Terjual')

    plt.ylim(0, tren_terlaris['jumlah_terjual'].max() + 1000)  # Beri ruang di atas supaya label jumlah tidak mepet

    # Menampilkan grafik
    st.pyplot(fig)


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
