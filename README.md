

# **Analisis Data Penjualan E-Commerce**  

## **Ringkasan Proyek**  
Proyek ini bertujuan untuk menganalisis data transaksi e-commerce guna memahami tren penjualan, kategori produk dengan performa terbaik, serta wawasan yang dapat digunakan untuk pengambilan keputusan bisnis.  

Dashboard interaktif dikembangkan menggunakan **Streamlit** untuk memudahkan eksplorasi data dan visualisasi.  

---

## **Fitur Utama**  
- Analisis kategori produk dengan penjualan tertinggi  
- Identifikasi pola penjualan berdasarkan tahun  
- Visualisasi data interaktif menggunakan **Plotly** dan **Matplotlib**  
- Navigasi yang intuitif dengan sidebar menu  
- Rekomendasi bisnis berdasarkan hasil analisis  

---

## **Struktur Direktori**  
```
📦 analisis-penjualan
├── 📂 dashboard/               # File untuk dashboard Streamlit
│   ├── dashboard.py            # Script utama dashboard
│   ├── main_data.csv           # Data hasil preprocessing
│
├── 📂 data/                    # Dataset mentah
│   ├── orders.csv
│   ├── order_items.csv
│   ├── products.csv
│   ├── customers.csv
│   ├── sellers.csv
│
├── all_data.csv                # Dataset gabungan
├── exploratory_analysis.ipynb   # Notebook eksplorasi data
├── README.md                   # Dokumentasi proyek
├── requirements.txt             # Pustaka yang dibutuhkan
└── deployment_link.txt          # (Opsional) Link deployment dashboard  
```

---

## **Panduan Penggunaan**  
### **1. Persiapan Awal**  
Pastikan Python dan pustaka yang diperlukan telah diinstal. Jika belum, jalankan perintah berikut:  

```bash
pip install -r requirements.txt
```

### **2. Menjalankan Dashboard**  
Gunakan perintah berikut di terminal untuk menjalankan aplikasi:  

```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan terbuka secara otomatis di browser.  

---

## **Hasil Analisis dan Wawasan**  
 ### **Kesimpulan dari 5 Kategori Produk Terlaris** ###  

1. **Bed Bath Table 12.718 Unit Terjual**  
   - Kategori dengan penjualan tertinggi dibandingkan kategori lain.  
   - Produk-produk dalam kategori ini (seperti perlengkapan kamar tidur dan kamar mandi) kemungkinan memiliki permintaan stabil dan pasar yang luas.  
   - Bisa menjadi kategori utama dalam strategi bisnis untuk meningkatkan profitabilitas.  

2. **Health & Beauty 9.670 Unit Terjual**  
   - Kategori ini memiliki permintaan tinggi, menunjukkan bahwa kesehatan dan kecantikan menjadi prioritas konsumen.  
   - Tren self-care dan beauty care kemungkinan menjadi faktor utama pertumbuhan kategori ini.  
   - Potensi besar untuk dikembangkan dengan menambah produk yang sesuai dengan tren pasar.  

3. **Sports & Leisure 8.641 Unit Terjual**  
   - Menandakan peningkatan minat masyarakat terhadap gaya hidup sehat dan olahraga.  
   - Bisa menjadi pasar potensial yang terus berkembang, terutama dengan tren kebugaran dan olahraga yang meningkat.  
   - Strategi pemasaran dapat diarahkan pada komunitas olahraga dan gaya hidup aktif.  

4. **Furniture & Decor 8.334 Unit Terjual**
   - Permintaan tinggi dalam kategori ini menunjukkan bahwa tren dekorasi rumah dan furniture meningkat
   - Bisa menjadi peluang untuk menjual produk inovatif yang menyesuaikan selera dan kebutuhan konsumen.  
   - Bisa ditingkatkan dengan promosi visual menarik dan pemasaran berbasis estetika.  

5. **Computers & Accessories  7.827 Unit Terjual**
   - Kategori teknologi tetap menjadi kebutuhan utama, terutama dengan meningkatnya tren work from home dan digitalisasi  
   - Permintaan tinggi untuk perangkat seperti laptop, aksesoris komputer, dan gadget pendukung lainnya.  
   - Potensi pertumbuhan tinggi jika fokus pada teknologi inovatif dan tren terbaru.  


### **Kesimpulan Tren Kategori dengan Penjualan Tertinggi Tiap Tahun** ###

1. **Tahun 2016: Furniture & Decor 65 Unit Terjual**  
   - Penjualan kategori tertinggi di tahun ini sangat rendah dibanding tahun-tahun berikutnya.  
   - Bisa jadi belum ada permintaan besar atau tren dekorasi rumah belum berkembang pesat.  
   - Tahun ini belum menunjukkan kategori yang mendominasi pasar.  

2. **Tahun 2017: Bed Bath Table 6.008 Unit Terjual**  
   - Lonjakan besar dalam penjualan dibandingkan tahun 2016.  
   - Kategori bed bath table mulai menjadi favorit konsumen, menunjukkan adanya tren yang berkembang dalam kebutuhan perlengkapan rumah tangga.  
   - Bisa jadi akibat meningkatnya kesadaran akan kenyamanan rumah dan perubahan gaya hidup.  

3. **Tahun 2018: Bed Bath Table 6.470 Unit Terjual**
   - Kategori Bed Bath Table masih mendominasi, bahkan mengalami kenaikan dari tahun sebelumnya.  
   - Permintaan terhadap produk ini terus meningkat, menunjukkan pasar yang stabil dan loyalitas pelanggan.  
   - Bisa menjadi sinyal bagi bisnis untuk terus mengembangkan kategori ini dengan inovasi produk atau pemasaran lebih luas.  
---

## **Teknologi yang Digunakan**  
- **Python** – Bahasa pemrograman utama  
- **Streamlit** – Pengembangan dashboard interaktif  
- **Pandas** – Manipulasi dan analisis data  
- **Plotly & Matplotlib** – Visualisasi data  
- **Jupyter Notebook** – Eksplorasi data  

---

## **Catatan Tambahan**  
Jika mengalami kendala saat menjalankan proyek, pastikan:  
✔ Semua pustaka telah diinstal dengan benar  
✔ Struktur folder sesuai dokumentasi  
✔ Dataset tersedia dalam folder `data/`  

