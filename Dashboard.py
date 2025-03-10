import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ---- Setup Streamlit ----
st.title("📊 Dashboard Penjualan E-Commerce")
st.write("Analisis data penjualan dan segmentasi pelanggan berdasarkan RFM Analysis.")

# ---- Load Data ----
orders = pd.read_csv("/mnt/data/orders_cleaned.csv")
order_items = pd.read_csv("/mnt/data/item_cleaned.csv")
payments = pd.read_csv("/mnt/data/review_cleaned.csv")
customers = pd.read_csv("/mnt/data/produk_cleaned.csv")

# ---- RFM Analysis ----
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
rfm_data = orders[['customer_id', 'order_id', 'order_purchase_timestamp']]

max_date = rfm_data['order_purchase_timestamp'].max()
recency = rfm_data.groupby('customer_id').order_purchase_timestamp.max().reset_index()
recency['Recency'] = (max_date - recency['order_purchase_timestamp']).dt.days

frequency = rfm_data.groupby('customer_id').order_id.nunique().reset_index()
frequency.columns = ['customer_id', 'Frequency']

monetary = payments.groupby('customer_id').payment_value.sum().reset_index()
monetary.columns = ['customer_id', 'Monetary']

df_rfm = recency.merge(frequency, on='customer_id').merge(monetary, on='customer_id')
df_rfm['R_Score'] = pd.qcut(df_rfm['Recency'], q=4, labels=[4, 3, 2, 1])
df_rfm['F_Score'] = pd.qcut(df_rfm['Frequency'].rank(method='first'), q=4, labels=[1, 2, 3, 4])
df_rfm['M_Score'] = pd.qcut(df_rfm['Monetary'], q=4, labels=[1, 2, 3, 4])
df_rfm['RFM_Score'] = df_rfm[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

def rfm_segment(score):
    if score >= 10:
        return 'Best Customers'
    elif score >= 8:
        return 'Loyal Customers'
    elif score >= 6:
        return 'Potential Loyalist'
    elif score >= 4:
        return 'At Risk'
    else:
        return 'Lost Customers'

df_rfm['Segment'] = df_rfm['RFM_Score'].astype(int).apply(rfm_segment)

# ---- Fitur Interaktif ----
st.sidebar.header("🔍 Filter")
segment_filter = st.sidebar.multiselect("Pilih Segmen Pelanggan:", options=df_rfm['Segment'].unique(), default=df_rfm['Segment'].unique())

filtered_rfm = df_rfm[df_rfm['Segment'].isin(segment_filter)]

st.subheader("📌 Distribusi Recency, Frequency, dan Monetary")
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
sns.histplot(filtered_rfm['Recency'], bins=30, kde=True, ax=axes[0])
axes[0].set_title('Distribusi Recency')
sns.histplot(filtered_rfm['Frequency'], bins=30, kde=True, ax=axes[1])
axes[1].set_title('Distribusi Frequency')
sns.histplot(filtered_rfm['Monetary'], bins=30, kde=True, ax=axes[2])
axes[2].set_title('Distribusi Monetary')
st.pyplot(fig)

st.write("📌 **Jumlah Pelanggan per Segmen:**")
st.bar_chart(filtered_rfm['Segment'].value_counts())

st.write("📌 **Tabel RFM Pelanggan:**")
st.dataframe(filtered_rfm)
