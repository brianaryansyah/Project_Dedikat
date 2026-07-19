# DEDIKAT: Deteksi Dini Penyakit Katarak Berbasis Analisis Citra Retina Digital

> **Proyek Akhir Praktikum Pemelajaran Mesin (Semester 4) — Universitas Dian Nuswantoro (UDINUS)**
> 
> * **Nama**: Brian Aryansyah Pamungkas
> * **NIM**: A11.2024.15880
> * **Kelompok**: A11.4405

---

## Deskripsi Proyek

DEDIKAT (Deteksi Dini Katarak) adalah sistem kecerdasan buatan (*Artificial Intelligence*) medis terpadu yang dirancang untuk melakukan penapisan awal (*screening*) dan lokalisasi spasial kekeruhan lensa mata (katarak) secara otomatis melalui analisis citra digital. Proyek ini mengintegrasikan dua pendekatan *deep learning* utama, yaitu algoritma **YOLOv8s** untuk lokalisasi objek patologis (*object detection* dengan *bounding box*) dan arsitektur **ResNet-50** untuk klasifikasi citra medis *end-to-end* tingkat tinggi. Dilengkapi dengan antarmuka berbasis web Flask kustom (premium dengan efek *before/after slider* klinis dan cetak laporan PDF otomatis) serta alternatif dasbor interaktif berbasis Streamlit, DEDIKAT bertujuan membantu para praktisi medis di daerah satelit melakukan skrining katarak secara efisien, akurat, dan transparan melalui integrasi teknologi *Explainable AI* (Grad-CAM, LIME, dan Saliency Maps).

---

## Akses Aplikasi Online (Live Demo)

Aplikasi DEDIKAT versi dasbor Streamlit telah dideploy secara online dan dapat langsung diakses oleh publik atau penguji melalui tautan berikut:
**[DEDIKAT Web App di Streamlit Cloud](https://dedikat-deteksidinikatarak-bybrian.streamlit.app/)**

---

## Dataset dan Eksplorasi Data

Proyek DEDIKAT dikembangkan menggunakan dataset **Cataract Eye Data** yang bersumber dari platform Kaggle:
* **Tautan Dataset**: [Kaggle - Cataract Eye Data by suyog17](https://www.kaggle.com/datasets/suyog17/cataracteyedata)
* **Penjelasan Dataset**:
  Dataset ini berisi kumpulan gambar mata berkualitas tinggi yang terbagi menjadi dua kelas utama secara seimbang:
  1. **Cataract (Mata Positif Katarak)**: Menampilkan citra mata dengan tingkat kekeruhan patologis yang bervariasi pada bagian lensa pupil.
  2. **Normal (Mata Sehat)**: Menampilkan kondisi mata sehat dengan lensa pupil yang jernih dan bebas dari tanda-tanda opasitas.
  Dataset ini digunakan untuk melatih model deteksi objek (anotasi bounding box melokalisasi area pupil katarak) serta model klasifikasi citra digital guna membedakan karakteristik mata sehat vs katarak.

---

## Fitur dan Inovasi Utama

* **Sistem Deteksi Ganda (YOLOv8s & ResNet-50)**: Penggabungan kemampuan lokalisasi lesi spasial (YOLOv8s) dan klasifikasi kategori *end-to-end* yang kuat (ResNet-50).
* **Interactive Before/After Slider**: Fitur penggeser vertikal responsif di halaman web untuk membandingkan secara langsung antara citra mata asli masukan pasien dan anotasi bounding box AI.
* **Cetak Laporan Medis Instan (Print Clinical PDF)**: Menyediakan tombol cetak otomatis yang memformat halaman web menjadi bentuk dokumen laporan diagnosis klinis resmi lengkap dengan tabel koordinat, diagram temuan, rekomendasi medis, dan lembar tanda tangan dokter penanggung jawab.
* **Explainable AI (XAI)**: Visualisasi tingkat transparansi model menggunakan **Grad-CAM**, **LIME**, **Saliency Maps**, serta proyeksi ruang fitur **PCA** dan **t-SNE** untuk memverifikasi keputusan AI berdasarkan bukti klinis secara ilmiah.
* **Hardware & Status Monitoring**: Widget pemantau real-time untuk mengecek server Flask lokal serta status penggunaan akselerasi perangkat keras GPU CUDA (seperti NVIDIA GeForce RTX 3050) vs CPU Mode.

---

## Pipeline Sistem

Alur pemrosesan data (pipeline) dalam aplikasi DEDIKAT dirancang secara sistematis dengan langkah-langkah berikut:

1. **Akuisisi Citra Masukan**: Pengguna mengunggah gambar mata (tampak depan/frontal) secara seret-lepas (*drag-and-drop*) atau menggunakan galeri tombol contoh medis katarak/normal.
2. **Pra-pemrosesan & Penyelarasan**: Gambar dibersihkan dari noise, disesuaikan kontrasnya, dan diubah dimensinya secara otomatis ke ukuran standar $640 \times 640$ piksel sebagai syarat input neural network.
3. **Inference Deep Learning**: Citra dikirim ke model YOLOv8s (melalui pustaka PyTorch) untuk memprediksi probabilitas kelas dan koordinat spasial bounding box.
4. **Penyaringan Hasil Logika (Penyelarasan Diagnosis)**: Sistem secara cerdas menyaring jenis deteksi. Jika hanya ditemukan deteksi kelas `Normal` (atau tanpa deteksi), status diagnosis bernilai **Negatif Katarak**. Jika ditemukan deteksi kelas `Cataract`, status didiagnosis sebagai **Positif Katarak**.
5. **Rendering Output & XAI**: Web menampilkan Before/After Slider interaktif, waktu proses, serta peta aktivasi Grad-CAM/LIME.
6. **Ekspor Hasil Laporan**: Pengguna dapat mencetak hasil diagnosis ke printer fisik atau menyimpannya sebagai berkas klinis berformat PDF.

---

## Struktur Repositori

```text
├── archive/                    # Folder arsip riwayat pelatihan & file riset lama
│   ├── base_models/            # Berkas model YOLOv8s & YOLOv8n asli (Base weights)
│   ├── plots/                  # Grafik plot riset data latih & kurva visualisasi lama
│   ├── runs/                   # Folder log & riwayat epoch pelatihan YOLOv8
│   └── scripts/                # Program utilitas pipeline pemrosesan lama
├── app/
│   ├── app.py                  # Backend Flask Server (Logika Router & API Deteksi)
│   ├── best.pt                 # File Bobot Model YOLOv8s Terlatih (Object Detection)
│   ├── resnet50_best.pth       # File Bobot Model ResNet-50 Terlatih (Image Classification)
│   ├── templates/
│   │   └── index.html          # File Web Template Utama Flask (Bebas emoji, responsif)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Lembar Gaya CSS (Skema Warna Medis Biru-Putih)
│   │   ├── js/
│   │   │   └── main.js         # Logika JS (Tab, Counter, Slider, dan AJAX)
│   │   └── images/             # Gambar riset & kurva evaluasi model terbaru
│   │       └── samples/        # Contoh citra klinis katarak & normal untuk uji cepat
│   └── copy_assets.py          # Utilitas untuk memindahkan gambar visualisasi riset
├── .streamlit/
│   └── config.toml             # Berkas konfigurasi tema warna Streamlit (Light Mode)
├── docs/
│   └── screenshots/            # Berkas gambar dokumentasi web untuk README.md
├── .gitignore                  # Berkas pengecualian Git (Mengabaikan file sampah & venv)
├── requirements.txt            # Berkas daftar dependensi pustaka Python (Streamlit Ready)
├── README.md                   # Dokumentasi repositori proyek DEDIKAT (Berkas ini)
├── streamlit_app.py            # Berkas alternatif web berbasis Streamlit (Deployment Ready)
├── train.ipynb                 # Jupyter Notebook proses pelatihan YOLOv8
├── train_resnet50.ipynb        # Jupyter Notebook proses pelatihan ResNet-50
└── train_resnet50.py           # Skrip pendukung proses pelatihan ResNet-50
```

---

## Panduan Instalasi dan Setup Lokal

### 1. Kloning repositori ini:
```bash
git clone https://github.com/brianaryansyah/Project_Dedikat.git
cd Project_Dedikat
```

### 2. Persiapkan Environment & Instalasi Pustaka
Anda bisa menggunakan **Conda** (direkomendasikan) atau **PIP** untuk mengelola dependensi program:

#### Pilihan A: Menggunakan Conda (Direkomendasikan untuk GPU/CUDA)
```bash
# Membuat environment Python 3.10
conda create -n sicasa_gpu python=3.10 -y
conda activate sicasa_gpu

# Pasang pustaka dependensi
pip install -r requirements.txt
```

#### Pilihan B: Menggunakan PIP (Virtual Environment Python Biasa)
```bash
# Membuat venv baru
python -m venv venv

# Mengaktifkan venv (Windows)
.\venv\Scripts\Activate.ps1
# Mengaktifkan venv (Linux/macOS)
source venv/bin/activate

# Pasang pustaka dependensi
pip install -r requirements.txt
```

### 3. Menjalankan Aplikasi Secara Lokal:

#### Opsi A: Menjalankan Versi Flask (Tampilan Premium & Custom)
Pastikan Anda berada di direktori root `Project_Dedikat`, lalu jalankan perintah:
```bash
python app/app.py
```
Aplikasi secara otomatis akan terbuka di browser Anda melalui **[http://localhost:5000](http://localhost:5000)**

#### Opsi B: Menjalankan Versi Streamlit (Dasbor Alternatif)
Pastikan Anda berada di direktori root `Project_Dedikat`, lalu jalankan perintah:
```bash
streamlit run streamlit_app.py
```
Aplikasi secara otomatis akan terbuka di browser Anda melalui **[http://localhost:8501](http://localhost:8501)**

---

## Dokumentasi Antarmuka Pengguna

### 1. Halaman Awal Web DEDIKAT
Menampilkan tata letak bersih bertema warna biru-putih Drone.io dengan tab demonstrasi model yang rapi.
![Halaman Awal Web](docs/screenshots/halaman_awal.png)

### 2. Hasil Deteksi Bounding Box YOLOv8s & Slider Perbandingan
Menampilkan demo hasil deteksi katarak lengkap dengan status diagnosis medis dan Before/After slider.
![Hasil Deteksi](docs/screenshots/hasil_deteksi.png)

### 3. Dashboard Exploratory Data Analysis (EDA)
Menampilkan grafik sebaran kelas dataset seimbang, dimensi piksel, dan letak spasial bounding box.
![Dashboard EDA](docs/screenshots/dashboard_eda.png)

### 4. Evaluasi & Perbandingan Model
Menampilkan tabel metrik performa model, Confusion Matrix, kurva ROC, dan kurva Loss pelatihan.
![Evaluasi Model](docs/screenshots/evaluasi_model.png)

### 5. Visualisasi Interpretasi Hasil (Explainable AI)
Menampilkan peta Grad-CAM, interpretasi piksel LIME, Saliency Maps, serta reduksi dimensi t-SNE.
![Interpretasi Hasil](docs/screenshots/interpretasi_hasil.png)

---

## Spesifikasi Teknologi

| Kategori | Teknologi |
| --- | --- |
| **Bahasa Pemrograman** | Python 3.10 |
| **Data Manipulation** | Pandas, NumPy |
| **Data Visualization** | Seaborn, Matplotlib |
| **Machine & Deep Learning** | PyTorch, Ultralytics YOLOv8s, ResNet-50, Scikit-Learn (KNN, Random Forest) |
| **Web Application Framework** | Flask (Premium Custom HTML/CSS/JS), Streamlit |
| **Web Deployment** | Streamlit Community Cloud |
| **Environment Tools** | Conda, Jupyter Notebook, Visual Studio Code |

---

## Spesifikasi Model dan Performa

Berikut adalah rincian spesifikasi arsitektur model kecerdasan buatan yang dikembangkan dalam proyek DEDIKAT beserta performa evaluasi masing-masing model.

### Spesifikasi Model

#### Spesifikasi Model Deteksi Objek (YOLOv8s)
| Komponen | Detail |
| :--- | :--- |
| Feature Extractor | CSPDarknet53 (Pre-trained on COCO) -> Multi-scale feature maps |
| Architecture | YOLOv8s (Anchor-free detection head + PANet neck) |
| Parameters | ~11.200.000 (11,2 M) |
| Input | Citra $640 \times 640$ piksel (RGB) |
| Output | Bounding Box ($x_{min}, y_{min}, x_{max}, y_{max}$), Class ID, Confidence Score [0, 1] |

#### Spesifikasi Model Klasifikasi Citra (ResNet-50)
| Komponen | Detail |
| :--- | :--- |
| Feature Extractor | ResNet-50 (Pre-trained on ImageNet-1K) -> 2048-d feature vector |
| Architecture | ResNet-50 (Convolutional Residual Network + Fully Connected Layer head) |
| Parameters | ~23.500.000 (23,5 M) |
| Input | Citra $224 \times 224$ piksel (RGB) |
| Output | Class Probability [0, 1] (Threshold $\ge 0,5$ untuk kelas Cataract) |

---

### Hyperparameter Tuning

Proses pelatihan dan penyetelan hyperparameter dilakukan secara ketat untuk mendapatkan hasil optimal pada masing-masing algoritma:

| Model | Hyperparameter | Nilai/Konfigurasi |
| :--- | :--- | :--- |
| **YOLOv8s** | Epochs | 300 |
| | Optimizer | Auto (SGD/AdamW) |
| | Learning Rate ($lr_0$) | 0,01 |
| | Final Learning Rate ($lrf$) | 0,01 |
| | Momentum | 0,937 |
| | Weight Decay | 0,0005 |
| | Image Size | $640 \times 640$ piksel |
| | Early Stopping (Patience) | 20 epochs |
| **ResNet-50** | Epochs | 30 |
| | Batch Size | 32 |
| | Optimizer | AdamW |
| | Learning Rate Phase 1 (Feature Extractor) | 0,001 |
| | Learning Rate Phase 2 (Fine-Tuning) | 0,0001 |
| | Learning Rate Scheduler | CosineAnnealingLR |
| | Weight Decay | $1 \times 10^{-4}$ |
| | Image Size | $224 \times 224$ piksel |
| | Loss Function | CrossEntropyLoss |
| | Early Stopping (Patience) | 7 epochs |
| **K-Nearest Neighbors (KNN)** | Jumlah Tetangga ($k$) | 5 |
| | Bobot Tetangga (Weights) | Distance (berdasarkan jarak terbalik) |
| | Metrik Jarak (Metric) | Minkowski ($p=2$, ekuivalen dengan Euclidean) |
| **Random Forest** | Jumlah Pohon (n_estimators) | 200 |
| | Kedalaman Maksimum (max_depth) | Tanpa Batas (None) |
| | Minimum Split (min_samples_split) | 5 |
| | Random State | 42 (RANDOM_SEED) |

---

### Performa Model

Evaluasi model dilakukan secara komprehensif pada data uji (*test set*). Berikut adalah perbandingan performa antara YOLOv8s, ResNet-50, serta dua model berbasis *machine learning* tradisional (KNN dan Random Forest) yang memanfaatkan ekstraksi fitur dari lapisan terakhir ResNet-50:

| Metrik | YOLOv8s | ResNet-50 | KNN | Random Forest |
| :--- | :---: | :---: | :---: | :---: |
| **Akurasi (Accuracy)** | 96,83% | 98,73% | **99,05%** | **99,05%** |
| **Presisi (Precision)** | 97,60% | 98,69% | **99,02%** | **99,02%** |
| **Sensitivitas / Recall** | 95,66% | 98,77% | **99,06%** | **99,06%** |
| **F1-Score** | 96,82% | 98,73% | **99,04%** | **99,04%** |
| **AUROC** | 68,76% | 99,73% | **99,99%** | 99,92% |
| **MCC** | N/A | 97,46% | **98,09%** | **98,09%** |
| **Cohen's Kappa** | N/A | 97,45% | **98,09%** | **98,09%** |
| **Log Loss** | N/A | 7,07% | **1,32%** | 3,47% |
| **Waktu Inferensi (per Citra)** | 29,3 ms | 8,5 ms | 0,71 ms | **0,26 ms** |
| **Ukuran File Model (MB)** | 64,0 MB | 90,0 MB | 22,12 MB | **0,56 MB** |

*Catatan: Nilai performa terbaik untuk setiap metrik klasifikasi dicetak tebal.*

**Confusion Matrix (ResNet-50)**:
* True Negative (TN) = 146
* False Positive (FP) = 1
* False Negative (FN) = 3
* True Positive (TP) = 165
*(Dievaluasi pada test set dengan total 315 citra)*

---

### Interpretasi Model (Explainable AI / XAI)

Untuk menjamin transparansi keputusan klinis kecerdasan buatan, sistem DEDIKAT menerapkan beberapa metode interpretasi model:

* **Grad-CAM (Gradient-weighted Class Activation Mapping)**: Menghasilkan peta panas (*heatmap*) visualisasi spasial pada lapisan konvolusi terakhir ResNet-50. Grad-CAM menghitung gradien kelas target terhadap fitur peta konvolusi untuk mengidentifikasi area pupil atau lensa mata yang memiliki kontribusi terbesar dalam diagnosis katarak.
* **Saliency Maps**: Visualisasi berbasis piksel yang menghitung gradien dari *loss function* terhadap piksel citra masukan. Teknik ini menunjukkan sensitivitas prediksi model terhadap perubahan kecil pada intensitas piksel tertentu, yang menyoroti batas-batas fisik kekeruhan pada lensa mata.
* **LIME (Local Interpretable Model-agnostic Explanations)**: Pendekatan interpretasi lokal dengan cara melakukan perturbasi (pengubahan acak) pada superpiksel citra masukan guna mengamati perubahan perilaku prediksi model. Superpiksel yang mendukung prediksi kelas katarak akan ditandai dengan warna hijau, sedangkan yang menentang ditandai dengan warna merah.
* **Visualisasi Ruang Fitur (PCA & t-SNE)**:
  * **PCA (Principal Component Analysis)**: Mereduksi fitur dimensi tinggi ($2048$-d dari lapisan pooling ResNet-50) secara linear menjadi 2 dimensi untuk memetakan distribusi global data katarak vs normal.
  * **t-SNE (t-Distributed Stochastic Neighbor Embedding)**: Metode reduksi dimensi non-linear yang sangat efektif untuk mengelompokkan kemiripan lokal, memvisualisasikan bagaimana representasi fitur katarak dan sehat terpisah secara jelas di ruang latent.

---

## Analisis Performa dan Evaluasi Model

Pengembangan DEDIKAT melibatkan pemantauan metrik evaluasi secara ketat selama pelatihan model deep learning guna menjamin akurasi diagnosis medis yang aman bagi pasien:

### Kurva Pelatihan dan Loss YOLOv8s
![Kurva Latih YOLOv8s](app/static/images/eval_yolov8_training.png)
* **Analisis**: Kurva *Loss* lokalisasi kotak pembatas (*box_loss*) dan klasifikasi (*cls_loss*) pada set pelatihan maupun validasi menunjukkan penurunan yang konvergen dan stabil hingga epoch 130. Model berhasil mencapai nilai **mAP50** sebesar **96.83%**, mengindikasikan sensitivitas dan akurasi pelokalisasian pupil mata yang mengalami katarak sangat presisi.

### Kurva Pelatihan ResNet-50
![Kurva Latih ResNet-50](app/static/images/eval_resnet_training.png)
* **Analisis**: Model klasifikasi gambar *end-to-end* ResNet-50 dilatih dan dipantau tingkat keakuratannya. Kurva menunjukkan laju *Accuracy* validasi melonjak cepat hingga menstabilkan diri pada akurasi puncak sebesar **98.73%**. Tingkat *Cross-Entropy Loss* yang terus menurun mendekati angka nol membuktikan model memiliki pemahaman klasifikasi visual yang optimal dan bebas dari tanda-tanda *overfitting*.

### Evaluasi Confusion Matrix
![Confusion Matrix ResNet-50](app/static/images/eval_confusion_matrix.png)
* **Analisis**: Confusion Matrix memperlihatkan performa luar biasa dalam memisahkan kelas normal dan katarak. Jumlah prediksi benar (True Positive dan True Negative) mendominasi secara signifikan, dengan tingkat kesalahan *False Negative* (pasien katarak yang terdiagnosis normal) yang mendekati nol. Hal ini sangat krusial dalam domain diagnosis medis untuk mencegah kesalahan kelalaian penanganan klinis.

### Kurva ROC dan Precision-Recall
![Kurva ROC](app/static/images/eval_roc_curve.png)
![Kurva Precision-Recall](app/static/images/eval_pr_curve.png)
* **Analisis**: Kurva ROC menunjukkan nilai **Area Under Curve (AUC)** mencapai **99.73%** untuk model ResNet-50, membuktikan performa pembeda kelas yang sangat unggul di berbagai ambang batas klasifikasi. Ditambah dengan kurva Precision-Recall yang melengkung tajam ke arah kanan atas, ini membuktikan model tetap mempertahankan tingkat kebenaran deteksi yang tinggi (Precision) meskipun sensitivitas penemuan objek (Recall) dipaksa ke tingkat maksimum.

### Analisis Signifikansi Fitur (Random Forest Feature Importance)
![Feature Importance Random Forest](app/static/images/eval_rf_feature_importance.png)
* **Analisis**: Grafik ini memetakan kontribusi fitur citra yang diekstraksi terhadap keputusan model ensembel Random Forest. Fitur intensitas warna dan tekstur kelabu di area spasial tengah (pupil) terbukti memiliki signifikansi kontribusi tertinggi. Hal ini membuktikan keputusan pengelompokan status katarak oleh kecerdasan buatan didasarkan pada perubahan opasitas kelensa pupil secara biologis, bukan bias latar belakang gambar.

---

## Referensi

Hemasri, C. C., Vijayalakshmi, M., & Jyotheesh, V. (2024). Redefining medicine: The power of generative AI in modern healthcare. *2024 5th International Conference on Smart Electronics and Communication (ICOSEC)*, 1293–1298. https://doi.org/10.1109/ICOSEC61587.2024.10722592

Huang, Y., Zheng, H., Li, Y., Zheng, F., Zhen, X., Qi, G., Shao, L., & Zheng, Y. (2024). Multi-constraint transferable generative adversarial networks for cross-modal brain image synthesis. *International Journal of Computer Vision*, 1–17. https://doi.org/10.1007/s11263-024-02109-4

Joshi, S., dkk. (2023). XAI Meets Ophthalmology: An Explainable Approach to Cataract Detection Using VGG-19 and Grad-CAM. *2023 IEEE Pune Section International Conference (PuneCon)*, 19. https://doi.org/10.1109/PuneCon58714.2023.10450053

Kaggle. (n.d.). *Cataract Eye Data* [Dataset]. Diambil dari https://www.kaggle.com/datasets/suyog17/cataracteyedata

Kumar, A., Nelson, L., & Gomathi, S. (2024). Cataract prediction with VGG19 architecture using the ocular disease dataset. *2024 2nd World Conference on Communication & Computing (WCONF)*. IEEE. https://doi.org/10.1109/WCONF61366.2024.10692071

Shanshank, Mitali, G. P., Anusha, G., & Shuani, B. (2025). GAN-Enhanced Hybrid Deep Learning with Explainable AI for Automated Cataract Diagnosis. *Journal of Medical Systems*.

Wang, J., Xu, Z., Zheng, W., Ying, H., Chen, T., Liu, Z., Chen, D. Z., Yao, K., & Wu, J. (2024). A transformer-based knowledge distillation network for cortical cataract grading. *IEEE Transactions on Medical Imaging*, 43(3), 1089–1101. https://doi.org/10.1109/TMI.2023.3327274

Yadav, S., & Yadav, J. K. P. S. (2023). Automatic cataract severity detection and grading using deep learning. *Journal of Sensors*, 34, 1–17. https://doi.org/10.1155/2023/2973836
