

# **Analisis Data Penjualan E-Commerce**  

## **Ringkasan Proyek**  
Proyek ini bertujuan untuk menganalisis data transaksi e-commerce guna memahami tren penjualan, kategori produk dengan performa terbaik, serta wawasan yang dapat digunakan untuk pengambilan keputusan bisnis.  

Dashboard interaktif dikembangkan menggunakan **Streamlit** untuk memudahkan eksplorasi data dan visualisasi.  

---

## **Fitur Utama**  
- Analisis kategori produk dengan penjualan tertinggi  
- Identifikasi pola penjualan berdasarkan tahun  
- Visualisasi data interaktif menggunakan **Plotly**,  **Matplotlib** dan **Seaborn**
- Navigasi yang intuitif dengan sidebar menu  
- Rekomendasi bisnis berdasarkan hasil analisis  

---

## **Struktur Direktori**  
PROYEK ANALISIS DATA  
├─── dashboard  
│    ├─── Dashboard_e_commerce.py  
│    ├─── produk_cleaned.csv  
│    ├─── item_cleaned.csv  
│    └─── orders_cleaned.csv  
│  
├─── data  
│    ├─── customers_dataset.csv  
│    ├─── geolocation_dataset.csv  
│    ├─── order_reviews_dataset.csv  
│    ├─── orders_dataset.csv  
│    ├─── orders_items_dataset.csv  
│    ├─── orders_payments_dataset.csv  
│    ├─── product_category_name_translation.csv  
│    ├─── product_dataset.csv  
│    ├─── products_dataset.csv  
│    ├─── sellers_dataset.csv  
│    └─── orders_items_dataset.csv  
│  
├─── Proyek_Analisis_Data_E_Commerce_Brazilian_Dataset.ipynb  
├─── README.md  
├─── requirements.txt  
└─── url.txt  


## **Instalasi & Menjalankan Aplikasi**  

### **1️⃣ Instal Dependensi**  
Pastikan Python dan pustaka yang diperlukan telah diinstal. Jika belum, jalankan perintah berikut: 
```bash
pip install -r requirements.txt
```
### **2️⃣ Jalankan Aplikasi Streamlit**  
Gunakan perintah berikut untuk menjalankan aplikasi:  
```bash
streamlit run "Dashboard e-commerce.py"
```
Setelah itu, buka browser dan akses **http://localhost:8501** untuk melihat dashboard.  
---

## **🚀 Deploy ke Streamlit Cloud**  

1. **Upload proyek ke GitHub.**  
2. **Buka Streamlit Cloud** – [https://share.streamlit.io](https://share.streamlit.io)  
3. **Hubungkan ke repo GitHub** dan pilih file `Dashboard e-commerce.py` sebagai entry point.  
4. Tunggu proses deploy selesai, lalu akses aplikasi di:  
   ```
   [Your Streamlit App URL]
   ```

---

## **Hasil Analisis dan Wawasan**  
- **Kesimpulan dari 5 Kategori Produk Terlaris**  
1. **Cama_mesa_banho 12.718 Unit Terjual**  
   - Kategori dengan penjualan tertinggi dibandingkan kategori lain.  
   - Produk-produk dalam kategori ini (seperti perlengkapan kamar tidur dan kamar mandi) kemungkinan memiliki permintaan stabil dan pasar yang luas.  
   - Bisa menjadi kategori utama dalam strategi bisnis untuk meningkatkan profitabilitas.  

2. **Beleza_saude 9.670 Unit Terjual**  
   - Kategori ini memiliki permintaan tinggi, menunjukkan bahwa kesehatan dan kecantikan menjadi prioritas konsumen.  
   - Tren self-care dan beauty care kemungkinan menjadi faktor utama pertumbuhan kategori ini.  
   - Potensi besar untuk dikembangkan dengan menambah produk yang sesuai dengan tren pasar.  

3. **Esporte_lazer 8.641 Unit Terjual**  
   - Menandakan peningkatan minat masyarakat terhadap gaya hidup sehat dan olahraga.  
   - Bisa menjadi pasar potensial yang terus berkembang, terutama dengan tren kebugaran dan olahraga yang meningkat.  
   - Strategi pemasaran dapat diarahkan pada komunitas olahraga dan gaya hidup aktif.  

4. **Moveis_decoracao 8.334 Unit Terjual**
   - Permintaan tinggi dalam kategori ini menunjukkan bahwa tren dekorasi rumah dan furniture meningkat
   - Bisa menjadi peluang untuk menjual produk inovatif yang menyesuaikan selera dan kebutuhan konsumen.  
   - Bisa ditingkatkan dengan promosi visual menarik dan pemasaran berbasis estetika.  

5. **Informatica_acessorios 7.827 Unit Terjual**
   - Kategori teknologi tetap menjadi kebutuhan utama, terutama dengan meningkatnya tren work from home dan digitalisasi  
   - Permintaan tinggi untuk perangkat seperti laptop, aksesoris komputer, dan gadget pendukung lainnya.  
   - Potensi pertumbuhan tinggi jika fokus pada teknologi inovatif dan tren terbaru.
   - 
- **Kesimpulan Tren Kategori dengan Penjualan Tertinggi Tiap Tahun**  
1. **Tahun 2016: Moveis_decoracao 65 Unit Terjual**  
   - Penjualan kategori tertinggi di tahun ini sangat rendah dibanding tahun-tahun berikutnya.  
   - Bisa jadi belum ada permintaan besar atau tren dekorasi rumah belum berkembang pesat.  
   - Tahun ini belum menunjukkan kategori yang mendominasi pasar.  

2. **Tahun 2017: Cama_mesa_banho 6.008 Unit Terjual**  
   - Lonjakan besar dalam penjualan dibandingkan tahun 2016.  
   - Kategori bed bath table mulai menjadi favorit konsumen, menunjukkan adanya tren yang berkembang dalam kebutuhan perlengkapan rumah tangga.  
   - Bisa jadi akibat meningkatnya kesadaran akan kenyamanan rumah dan perubahan gaya hidup.  

3. **Tahun 2018: Cama_mesa_banho 6.470 Unit Terjual**
   - Kategori ini masih mendominasi, bahkan mengalami kenaikan dari tahun sebelumnya.  
   - Permintaan terhadap produk ini terus meningkat, menunjukkan pasar yang stabil dan loyalitas pelanggan.  
   - Bisa menjadi sinyal bagi bisnis untuk terus mengembangkan kategori ini dengan inovasi produk atau pemasaran lebih luas.  
---

## **Teknologi yang Digunakan**  
- **Python** – Bahasa pemrograman utama  
- **Streamlit** – Pengembangan dashboard interaktif  
- **Pandas** – Manipulasi dan analisis data  
- **NumPy** – Operasi numerik dan manipulasi array  
- **Matplotlib & Seaborn** – Visualisasi data  
- **Plotly** – Grafik interaktif  
- **Babel** – Format angka dan mata uang  
- **Google Colab** – Pengolahan dan eksplorasi data di cloud

---

## **Catatan Tambahan**  
Jika mengalami kendala saat menjalankan proyek, pastikan:  
✔ Semua pustaka telah diinstal dengan benar  
✔ Struktur folder sesuai dokumentasi  
✔ Dataset tersedia dalam folder `data/`  

