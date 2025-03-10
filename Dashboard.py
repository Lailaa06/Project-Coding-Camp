import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned dataset
@st.cache_data
def load_data():
    df_rfm = pd.read_csv("cleaned_rfm_data.csv")  # Gantilah dengan file hasil analisismu
    return df_rfm

df_rfm = load_data()

# Sidebar Filters
years = df_rfm['year'].unique() if 'year' in df_rfm.columns else []
selected_year = st.sidebar.selectbox("Filter Tahun", years) if years.any() else None

categories = df_rfm['category'].unique() if 'category' in df_rfm.columns else []
selected_category = st.sidebar.selectbox("Pilih Kategori Produk", categories) if categories.any() else None

# Filter Data
if selected_year:
    df_rfm = df_rfm[df_rfm['year'] == selected_year]
if selected_category:
    df_rfm = df_rfm[df_rfm['category'] == selected_category]

# Dashboard Title
st.title("📊 RFM Analysis Dashboard")

# Pie Chart Segmen Pelanggan
st.subheader("Distribusi Segmen Pelanggan")
fig_segment = px.pie(df_rfm, names='Segment', title='Distribusi Segmen Pelanggan', hole=0.4)
st.plotly_chart(fig_segment)

# Scatter Plot: Frequency vs Monetary
st.subheader("Hubungan Frequency vs Monetary")
fig_scatter = px.scatter(df_rfm, x='Frequency', y='Monetary', color='Segment', title='Scatter Plot Frequency vs Monetary')
st.plotly_chart(fig_scatter)

# Histogram Recency, Frequency, Monetary
st.subheader("Distribusi Recency")
fig_recency = px.histogram(df_rfm, x='Recency', nbins=30, title='Distribusi Recency')
st.plotly_chart(fig_recency)

st.subheader("Distribusi Frequency")
fig_frequency = px.histogram(df_rfm, x='Frequency', nbins=30, title='Distribusi Frequency')
st.plotly_chart(fig_frequency)

st.subheader("Distribusi Monetary")
fig_monetary = px.histogram(df_rfm, x='Monetary', nbins=30, title='Distribusi Monetary')
st.plotly_chart(fig_monetary)

# Menampilkan Dataframe
st.subheader("📋 Data Pelanggan RFM")
st.dataframe(df_rfm)
