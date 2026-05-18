# Retail Crisis & Recovery Visualization Challenge

Project analisis data berbasis Python yang dibuat untuk mengikuti Hackathon Python DQLab x UjiKompetensi dengan studi kasus Retail Crisis & Recovery.  

Project ini berfokus pada identifikasi produk rising star, analisis pola pembelian pelanggan menggunakan algoritma Apriori, serta visualisasi tren penjualan dan recovery bisnis menggunakan Python.

---

# Challenge Overview

DQFresh Mart Retail mengalami penurunan total nilai penjualan dalam beberapa bulan terakhir.  

Melalui analisis data transaksi penjualan, ditemukan bahwa beberapa produk yang terlihat kecil ternyata memiliki tren pertumbuhan yang konsisten namun sering tidak terlihat dalam dashboard utama karena kontribusi revenue yang masih rendah.

Challenge ini bertujuan untuk:
- Mengidentifikasi produk dengan tren pertumbuhan tinggi (Rising Star)
- Menganalisis pola pembelian pelanggan
- Membuat visualisasi recovery dan performance trend
- Menyajikan insight bisnis berbasis data menggunakan Python

---

# Metode Analisis

### Rising Star Detection
- Moving Average 3 hari
- Identifikasi consecutive rising trend
- Filter minimal 12 hari kenaikan berturut-turut
- Perhitungan growth percentage

### Market Basket Analysis
- Algoritma Apriori (`mlxtend`)
- Minimum support 1%
- Association Rules dengan metric lift
- Filtering rules berdasarkan produk rising star

### Visualisasi
- Performance Index (Base 100)
- Actual Sales Trend Visualization

---

# Features

- Rising Star Product Detection
- Market Basket Analysis
- Performance Index Visualization
- Actual Sales Trend Visualization
- Export Insight Otomatis ke Excel
- High Resolution Visualization

---

# Teknologi

- Python
- Pandas
- NumPy
- Matplotlib
- Mlxtend
- OpenPyXL
---

# Acknowledgements

- [DQLab](https://dqlab.id/)
- [UjiKompetensi](https://ujikompetensi.com/)

---

# Author

Aprilia Marenden
