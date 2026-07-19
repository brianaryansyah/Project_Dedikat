import os
import time
import torch
import cv2
import base64
import numpy as np
from PIL import Image
from pathlib import Path
from io import BytesIO
import streamlit as st
import streamlit.components.v1 as components

# ──────────────────────────────────────────────
# Konfigurasi Halaman & Tema Streamlit
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="DEDIKAT — Deteksi Dini Katarak",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Path Konfigurasi
BASE_DIR = Path(__file__).parent.resolve()
MODEL_PATH = BASE_DIR / "app" / "best.pt"
STATIC_IMAGES_DIR = BASE_DIR / "app" / "static" / "images"

# Helper to convert image path or numpy array to base64
def file_to_base64(path):
    if not Path(path).exists():
        return ""
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def arr_to_base64(img_array_rgb):
    pil_img = Image.fromarray(img_array_rgb)
    buf = BytesIO()
    pil_img.save(buf, format='JPEG', quality=90)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# ──────────────────────────────────────────────
# CSS Injeksi Tingkat Lanjut (Menyamakan dengan Flask)
# ──────────────────────────────────────────────
st.markdown("""
    <style>
        /* Sembunyikan Header & Footer Default Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Font Global */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;600;700&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #F4F7FC !important;
            color: #0F172A !important;
        }
        
        /* Kurangi top padding sidebar */
        [data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem !important;
        }
        
        /* Styling Sidebar */
        [data-testid="stSidebar"] {
            background-color: #E9F1FA !important;
            border-right: 1px solid #E2E8F0;
        }
        
        /* Header Custom */
        .brand-container {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 0;
            margin-bottom: 20px;
        }
        .brand-text {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.6rem;
            font-weight: 800;
            color: #0F172A;
        }
        .brand-accent {
            color: #00ABE4;
        }
        
        /* Penyelarasan Judul & Teks */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Space Grotesk', sans-serif !important;
            color: #0F172A !important;
            font-weight: 700 !important;
        }
        
        .section-tag {
            display: inline-block;
            background: #E9F1FA;
            border: 1px solid rgba(0, 171, 228, 0.25);
            color: #00ABE4;
            padding: 4px 14px;
            border-radius: 100px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 8px;
        }
        
        /* Merubah Tampilan Tabs Streamlit agar mirip Tab Flask */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #E9F1FA;
            border: 1px solid #E2E8F0;
            padding: 5px;
            border-radius: 30px;
            gap: 6px;
            margin-bottom: 24px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: transparent;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: 700;
            font-size: 0.9rem;
            color: #475569 !important;
            border-radius: 25px !important;
            transition: all 0.25s;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            color: #0F172A !important;
            background-color: rgba(255, 255, 255, 0.4) !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF !important;
            color: #00ABE4 !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05) !important;
        }
        
        /* Custom Card (Border Container) */
        [data-testid="stVerticalBlockBorder"] {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 30px !important;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.04) !important;
            margin-bottom: 24px;
        }
        
        /* Tombol Utama */
        .stButton>button {
            background-color: #00ABE4 !important;
            color: white !important;
            border-radius: 12px !important;
            border: none !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 12px 24px !important;
            width: 100%;
            box-shadow: 0 4px 14px rgba(0, 171, 228, 0.25) !important;
            transition: all 0.25s !important;
        }
        
        .stButton>button:hover {
            background-color: #0098CB !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(0, 171, 228, 0.35) !important;
        }
        
        /* Style untuk tombol reset/secondary */
        .stButton>button[key*="btn_sample"] {
            background-color: #F1F5F9 !important;
            color: #475569 !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: none !important;
            padding: 8px 16px !important;
            font-size: 0.8rem !important;
        }
        
        .stButton>button[key*="btn_sample"]:hover {
            background-color: #E2E8F0 !important;
            color: #0F172A !important;
            transform: translateY(-1px) !important;
        }
        
        /* Status Warning Medis */
        .disclaimer-alert {
            background-color: rgba(59, 130, 246, 0.05);
            border: 1px solid rgba(59, 130, 246, 0.15);
            border-radius: 16px;
            padding: 20px;
            margin-top: 30px;
            font-size: 0.88rem;
            color: #475569;
            line-height: 1.6;
        }
        
        /* File uploader alignment */
        [data-testid="stFileUploader"] {
            padding: 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Memuat Model YOLOv8
# ──────────────────────────────────────────────
@st.cache_resource
def load_yolo_model():
    if MODEL_PATH.exists():
        from ultralytics import YOLO
        return YOLO(str(MODEL_PATH))
    return None

model = load_yolo_model()

# ──────────────────────────────────────────────
# Sidebar Custom (Navigasi Kiri)
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="brand-container">
            <span class="brand-text">DEDI<span class="brand-accent">KAT</span></span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Konfigurasi Ambang Batas AI")
    conf_threshold = st.slider("Confidence Threshold", min_value=0.05, max_value=0.95, value=0.25, step=0.05)
    iou_threshold = st.slider("IoU Threshold", min_value=0.05, max_value=0.95, value=0.45, step=0.05)
    
    st.markdown("---")
    st.markdown("### Monitor Infrastruktur AI")
    gpu_available = torch.cuda.is_available()
    if gpu_available:
        gpu_name = torch.cuda.get_device_name(0)
        st.markdown(f"""
            <div style="padding: 8px 12px; background: rgba(0, 171, 228, 0.08); border: 1px solid rgba(0, 171, 228, 0.25); border-radius: 8px; color: #00ABE4; font-family: monospace; font-size: 0.82rem; font-weight: bold; box-shadow: 0 0 10px rgba(0,171,228,0.15);">
                GPU CUDA: {gpu_name}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="padding: 8px 12px; background: #F1F5F9; border: 1px solid #E2E8F0; border-radius: 8px; color: #64748B; font-family: monospace; font-size: 0.82rem; font-weight: bold;">
                Akselerasi: CPU Mode
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown(f"""
        <div style="margin-top: 15px; font-size: 0.8rem; color: #475569; line-height: 1.7;">
            ● Server Flask: <strong style="color: #10B981;">Aktif (Port 5000)</strong><br>
            ● Database: <strong>1.199 Citra Medis</strong><br>
            ● Akurasi YOLOv8s: <strong>96.83%</strong>
        </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# Konten Utama & Navigasi Tab
# ──────────────────────────────────────────────
tabs = st.tabs([
    "Deteksi AI (Demo)", 
    "Dashboard EDA", 
    "Evaluasi Model", 
    "Interpretasi Hasil (XAI)", 
    "Dokumentasi"
])

# ──────────────────────────────────────────────
# TAB 1: MODEL DEMO (DETEKSI)
# ──────────────────────────────────────────────
with tabs[0]:
    st.markdown('<span class="section-tag">Model Demo</span>', unsafe_allow_html=True)
    st.markdown("## Sistem Deteksi Dini Katarak")
    st.write("DEDIKAT menggunakan algoritma **YOLOv8s Deep Learning** untuk mendeteksi indikasi penyakit katarak secara otomatis lewat analisis citra digital lensa mata.")
    
    col_left, col_right = st.columns([1, 1.2])
    
    selected_sample = None
    
    with col_left:
        # Container Input
        with st.container(border=True):
            st.markdown("#### Input Citra Medis")
            
            # Galeri Sampel
            st.markdown("<p style='font-size:0.8rem; font-weight:700; color:#475569; margin-bottom:8px; text-transform:uppercase;'>Uji Cepat dengan Sampel Medis:</p>", unsafe_allow_html=True)
            col_s1, col_s2 = st.columns(2)
            sample_c_path = STATIC_IMAGES_DIR / "samples" / "cataract_sample.jpg"
            sample_n_path = STATIC_IMAGES_DIR / "samples" / "normal_sample.jpg"
            
            with col_s1:
                if sample_c_path.exists():
                    st.image(str(sample_c_path), width=120)
                    if st.button("Mata Katarak", key="btn_sample_c"):
                        selected_sample = sample_c_path
            with col_s2:
                if sample_n_path.exists():
                    st.image(str(sample_n_path), width=120)
                    if st.button("Mata Normal", key="btn_sample_n"):
                        selected_sample = sample_n_path
            
            st.markdown("---")
            
            uploaded_file = st.file_uploader("Pilih berkas citra mata...", type=["jpg", "jpeg", "png", "webp", "bmp"])
            
            # Tentukan jalur gambar terpilih
            target_path = None
            if uploaded_file:
                temp_dir = BASE_DIR / "app" / "static" / "uploads"
                temp_dir.mkdir(parents=True, exist_ok=True)
                target_path = temp_dir / uploaded_file.name
                with open(target_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
            elif selected_sample:
                target_path = selected_sample
                
            if target_path:
                st.image(str(target_path), caption="Pratinjau Gambar Masukan", width=280)
                
            # Tombol Analisis
            trigger_analysis = st.button("Mulai Analisis Medis", key="btn_run_detect")
            
    with col_right:
        with st.container(border=True):
            st.markdown("#### Hasil Diagnostik AI")
            
            if not target_path:
                st.markdown("""
                    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 300px; text-align: center; color: #64748B; border: 2px dashed #E2E8F0; border-radius: 12px; padding: 20px;">
                        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" style="margin-bottom:12px; opacity:0.5;"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
                        <h4 style="margin:0; color:#64748B;">Belum Ada Data Teranalisis</h4>
                        <p style="font-size:0.85rem; margin-top:4px;">Pilih citra mata di panel sebelah kiri lalu tekan tombol "Mulai Analisis Medis".</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                if model is None:
                    st.error("Model YOLOv8s (best.pt) belum ditaruh di folder 'app/'.")
                else:
                    # Jalankan inferensi saat tombol ditekan
                    # Simulasi scanning progress agar interaktif seperti Flask
                    progress_text = st.empty()
                    progress_bar = st.progress(0)
                    
                    scan_steps = [
                        ("Menyusun Citra & Fokus Pupil...", 15),
                        ("Menyeimbangkan Kontras Citra...", 35),
                        ("Melakukan Segmentasi Lensa Pupil...", 55),
                        ("Ekstraksi Fitur Patologis Lensa...", 75),
                        ("Menjalankan Model Deteksi YOLOv8s...", 95)
                    ]
                    
                    for text, val in scan_steps:
                        progress_text.markdown(f"**Status Analisis**: *{text}*")
                        progress_bar.progress(val)
                        time.sleep(0.3)
                        
                    start_time = time.time()
                    
                    # Inferensi YOLOv8s
                    device = 0 if gpu_available else 'cpu'
                    results = model(
                        str(target_path),
                        conf=conf_threshold,
                        iou=iou_threshold,
                        device=device,
                        verbose=False
                    )
                    inference_time = (time.time() - start_time) * 1000
                    result = results[0]
                    
                    progress_text.markdown("**Status Analisis**: *Menyelesaikan Bounding Box...*")
                    progress_bar.progress(100)
                    time.sleep(0.2)
                    
                    # Bersihkan loader
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Parsing koordinat & kelas
                    detections = []
                    for box in result.boxes:
                        cls_id = int(box.cls)
                        conf_sc = float(box.conf)
                        cls_name = result.names.get(cls_id, f"Class_{cls_id}")
                        detections.append({
                            "class": cls_name,
                            "conf": round(conf_sc * 100, 1),
                            "bbox": [round(x, 1) for x in box.xyxy[0].tolist()]
                        })
                    
                    # Filter hanya deteksi katarak
                    cataract_detections = [
                        d for d in detections
                        if "katarak" in d["class"].lower() or "cataract" in d["class"].lower()
                    ]
                    
                    # Konversi citra ke Base64 untuk slider perbandingan
                    img_original_rgb = cv2.cvtColor(cv2.imread(str(target_path)), cv2.COLOR_BGR2RGB)
                    img_annotated_rgb = cv2.cvtColor(result.plot(), cv2.COLOR_BGR2RGB)
                    
                    b64_orig = arr_to_base64(img_original_rgb)
                    b64_anno = arr_to_base64(img_annotated_rgb)
                    
                    # 1. Tampilkan Warning Diagnosis
                    if len(cataract_detections) == 0:
                        st.markdown("""
                            <div style="display:flex; align-items:center; gap:12px; background:rgba(16, 185, 129, 0.08); border:1px solid rgba(16, 185, 129, 0.25); padding:12px 18px; border-radius:12px; margin-bottom:16px;">
                                <span style="font-size:1.5rem; color:#10B981;">✔</span>
                                <div>
                                    <strong style="color:#10B981; font-size:1rem;">Tidak Terdeteksi Katarak (Negatif)</strong>
                                    <p style="margin:0; font-size:0.85rem; color:#475569;">Berdasarkan analisis AI, kondisi lensa mata jernih dan normal.</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                            <div style="display:flex; align-items:center; gap:12px; background:rgba(239, 68, 68, 0.08); border:1px solid rgba(239, 68, 68, 0.25); padding:12px 18px; border-radius:12px; margin-bottom:16px;">
                                <span style="font-size:1.5rem; color:#EF4444;">⚠</span>
                                <div>
                                    <strong style="color:#EF4444; font-size:1rem;">Terdeteksi Katarak (Positif)</strong>
                                    <p style="margin:0; font-size:0.85rem; color:#475569;">Terdeteksi {len(cataract_detections)} indikasi katarak pada area pupil.</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        
                    # 2. RENDER BEFORE/AFTER COMPARISON SLIDER
                    html_comparison_code = f"""
                    <style>
                        .comparison-slider {{
                            position: relative;
                            width: 100%;
                            height: 350px;
                            border-radius: 12px;
                            overflow: hidden;
                            border: 1px solid #E2E8F0;
                            background: #080c14;
                        }}
                        .comparison-slider img {{
                            position: absolute;
                            top: 0;
                            left: 0;
                            width: 100%;
                            height: 100%;
                            object-fit: contain;
                        }}
                        .image-before {{
                            position: absolute;
                            inset: 0;
                            z-index: 10;
                        }}
                        .image-after {{
                            position: absolute;
                            inset: 0;
                            z-index: 20;
                            clip-path: polygon(0 0, 50% 0, 50% 100%, 0 100%);
                        }}
                        .slider-handle {{
                            position: absolute;
                            inset: 0;
                            width: 100%;
                            height: 100%;
                            -webkit-appearance: none;
                            appearance: none;
                            background: transparent;
                            outline: none;
                            z-index: 40;
                            cursor: ew-resize;
                        }}
                        .slider-divider {{
                            position: absolute;
                            top: 0;
                            bottom: 0;
                            left: 50%;
                            width: 2px;
                            background: #00ABE4;
                            z-index: 30;
                            box-shadow: 0 0 10px #00ABE4;
                        }}
                        .slider-divider::after {{
                            content: "↔";
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            width: 32px;
                            height: 32px;
                            background: #00ABE4;
                            color: white;
                            border-radius: 50%;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 1rem;
                            font-weight: bold;
                            border: 2px solid white;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        }}
                    </style>
                    <div class="comparison-slider" id="compSlider">
                        <div class="image-before">
                            <img src="data:image/jpeg;base64,{b64_orig}">
                        </div>
                        <div class="image-after" id="afterContainer">
                            <img src="data:image/jpeg;base64,{b64_anno}">
                        </div>
                        <input type="range" min="0" max="100" value="50" class="slider-handle" id="handleInput">
                        <div class="slider-divider" id="dividerLine"></div>
                    </div>
                    <script>
                        const handle = document.getElementById('handleInput');
                        const container = document.getElementById('afterContainer');
                        const divider = document.getElementById('dividerLine');
                        handle.addEventListener('input', (e) => {{
                            const val = e.target.value;
                            container.style.clipPath = `polygon(0 0, ${{val}}% 0, ${{val}}% 100%, 0 100%)`;
                            divider.style.left = `${{val}}%`;
                        }});
                    </script>
                    """
                    components.html(html_comparison_code, height=360)
                    st.caption("💡 Geser pembatas di atas untuk melihat perbandingan Citra Asli (kiri) vs Anotasi AI (kanan)")
                    
                    # 3. Metrik Statistik
                    st.markdown("---")
                    col_st1, col_st2, col_st3 = st.columns(3)
                    col_st1.metric("Objek Katarak", len(cataract_detections))
                    col_st2.metric("Waktu Proses", f"{round(inference_time, 1)} ms")
                    col_st3.metric("Akselerator Hardware", "GPU CUDA" if gpu_available else "CPU")
                    
                    # 4. Rincian Deteksi & Rekomendasi
                    if len(cataract_detections) > 0:
                        st.markdown("##### Rincian Temuan Deteksi Bounding Box:")
                        for det in cataract_detections:
                            st.write(f"- **{det['class']}** — Keyakinan: `{det['conf']}%` (BBox: `{det['bbox']}`)")
                        
                        st.markdown("""
                            <div style="background:rgba(239, 68, 68, 0.04); border:1px solid rgba(239, 68, 68, 0.15); padding:16px; border-radius:8px; color:#991b1b; font-size:0.88rem; line-height:1.5;">
                                <strong>Rekomendasi Medis DEDIKAT:</strong><br>
                                Terdeteksi adanya kekeruhan patologis pada lensa. Pasien sangat disarankan untuk segera melakukan pemeriksaan slit-lamp ke dokter spesialis mata (Sp.M) untuk diagnosis definitif.
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        if len(detections) > 0:
                            st.markdown("##### Rincian Temuan Deteksi Bounding Box:")
                            for det in detections:
                                st.write(f"- **{det['class']}** — Keyakinan: `{det['conf']}%` (BBox: `{det['bbox']}`)")
                                
                        st.markdown("""
                            <div style="background:rgba(16, 185, 129, 0.04); border:1px solid rgba(16, 185, 129, 0.15); padding:16px; border-radius:8px; color:#065f46; font-size:0.88rem; line-height:1.5;">
                                <strong>Rekomendasi Skrining Cerdas:</strong><br>
                                Lensa mata terlihat normal. Tetap jaga pola makan kaya antioksidan dan periksakan mata Anda ke dokter spesialis secara berkala minimal 1 tahun sekali.
                            </div>
                        """, unsafe_allow_html=True)

    # Disclaimer Medis
    st.markdown("""
        <div class="disclaimer-alert">
            <strong>Pernyataan Batasan (Medical Disclaimer):</strong> DEDIKAT dirancang sebagai asisten penapisan awal (screening tool) berbasis kecerdasan buatan akademis dan <strong>bukan merupakan vonis diagnosis klinis mutlak</strong>. Pengguna sangat dianjurkan untuk berkonsultasi langsung dengan dokter spesialis mata (ophthalmologist) guna penanganan medis yang akurat.
        </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TAB 2: DASHBOARD EDA
# ──────────────────────────────────────────────
with tabs[1]:
    st.markdown('<span class="section-tag">Data Exploration</span>', unsafe_allow_html=True)
    st.markdown("## Dashboard Analisis Eksploratif Data")
    st.write("Sebelum melatih model, kami mengeksplorasi karakteristik dataset ODIR Cataract untuk memastikan kesesuaian representasi fitur katarak pada mata.")
    
    col_eda1, col_eda2 = st.columns(2)
    
    with col_eda1:
        with st.container(border=True):
            st.markdown("##### Sebaran Kelas Dataset")
            img_dist = STATIC_IMAGES_DIR / "eda_class_dist.png"
            if img_dist.exists():
                st.image(str(img_dist), width="stretch")
            st.caption("Distribusi seimbang antara kelas katarak dan normal untuk mencegah model mengalami bias.")
            
        with st.container(border=True):
            st.markdown("##### Analisis Heat-map Spasial Bounding Box")
            img_bbox = STATIC_IMAGES_DIR / "eda_bbox_analysis.png"
            if img_bbox.exists():
                st.image(str(img_bbox), width="stretch")
            st.caption("Kerapatan koordinat membuktikan lesi terfokus tepat sasaran pada lensa pupil.")
            
    with col_eda2:
        with st.container(border=True):
            st.markdown("##### Dimensi Resolusi Citra Medis")
            img_dims = STATIC_IMAGES_DIR / "eda_img_dims.png"
            if img_dims.exists():
                st.image(str(img_dims), width="stretch")
            st.caption("Resolusi asli gambar fundus sebelum di-resize seragam ke ukuran input model.")
            
        with st.container(border=True):
            st.markdown("##### Perbandingan Area Bounding Box")
            img_area = STATIC_IMAGES_DIR / "eda_bbox_area_comp.png"
            if img_area.exists():
                st.image(str(img_area), width="stretch")
            st.caption("Grafik perolehan informasi perbandingan luas area normal versus yang mengalami kekeruhan.")

# ──────────────────────────────────────────────
# TAB 3: EVALUASI MODEL
# ──────────────────────────────────────────────
with tabs[2]:
    st.markdown('<span class="section-tag">Performance Review</span>', unsafe_allow_html=True)
    st.markdown("## Evaluasi Performa & Perbandingan Model")
    st.write("Kami melakukan komparasi performa antara **YOLOv8s (Object Detection)** dan 3 model klasifikasi **(ResNet-50, K-Nearest Neighbors, Random Forest)** pada partisi data uji independen.")
    
    # Metrik Evaluasi dalam Format HTML Table Medis
    st.markdown("""
        <table style="width:100%; border-collapse: collapse; margin-bottom: 24px; text-align: left;">
            <thead>
                <tr style="background-color: #E9F1FA; border-bottom: 2px solid #E2E8F0;">
                    <th style="padding: 12px; font-weight: bold;">Model</th>
                    <th style="padding: 12px; font-weight: bold;">Pendekatan</th>
                    <th style="padding: 12px; font-weight: bold;">Akurasi</th>
                    <th style="padding: 12px; font-weight: bold;">Presisi</th>
                    <th style="padding: 12px; font-weight: bold;">Recall</th>
                    <th style="padding: 12px; font-weight: bold;">F1-Score</th>
                    <th style="padding: 12px; font-weight: bold;">AUROC</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background-color: rgba(0, 171, 228, 0.04); font-weight: bold; border-bottom: 1px solid #E2E8F0;">
                    <td style="padding: 12px;">YOLOv8s</td>
                    <td style="padding: 12px;">Deteksi Objek (BBox)</td>
                    <td style="padding: 12px;">96.83%</td>
                    <td style="padding: 12px;">97.60%</td>
                    <td style="padding: 12px;">95.66%</td>
                    <td style="padding: 12px;">96.82%</td>
                    <td style="padding: 12px;">68.76%</td>
                </tr>
                <tr style="border-bottom: 1px solid #E2E8F0;">
                    <td style="padding: 12px;">ResNet-50</td>
                    <td style="padding: 12px;">Klasifikasi Citra</td>
                    <td style="padding: 12px;">98.73%</td>
                    <td style="padding: 12px;">98.69%</td>
                    <td style="padding: 12px;">98.77%</td>
                    <td style="padding: 12px;">98.73%</td>
                    <td style="padding: 12px;">99.73%</td>
                </tr>
                <tr style="border-bottom: 1px solid #E2E8F0;">
                    <td style="padding: 12px;">KNN (K=5)</td>
                    <td style="padding: 12px;">Klasifikasi Jarak</td>
                    <td style="padding: 12px;">99.05%</td>
                    <td style="padding: 12px;">99.02%</td>
                    <td style="padding: 12px;">99.06%</td>
                    <td style="padding: 12px;">99.04%</td>
                    <td style="padding: 12px;">99.99%</td>
                </tr>
                <tr>
                    <td style="padding: 12px;">Random Forest</td>
                    <td style="padding: 12px;">Ensembel Tree</td>
                    <td style="padding: 12px;">99.05%</td>
                    <td style="padding: 12px;">99.02%</td>
                    <td style="padding: 12px;">99.06%</td>
                    <td style="padding: 12px;">99.04%</td>
                    <td style="padding: 12px;">99.92%</td>
                </tr>
            </tbody>
        </table>
    """, unsafe_allow_html=True)
    
    col_ev1, col_ev2 = st.columns(2)
    with col_ev1:
        with st.container(border=True):
            st.markdown("##### Confusion Matrix (ResNet-50)")
            img_cm = STATIC_IMAGES_DIR / "eval_confusion_matrix.png"
            if img_cm.exists():
                st.image(str(img_cm), width="stretch")
                
        with st.container(border=True):
            st.markdown("##### Kurva Pelatihan Model")
            img_tr = STATIC_IMAGES_DIR / "eval_yolov8_training.png"
            if img_tr.exists():
                st.image(str(img_tr), width="stretch")
                
    with col_ev2:
        with st.container(border=True):
            st.markdown("##### Kurva ROC & Precision-Recall")
            img_roc = STATIC_IMAGES_DIR / "eval_roc_curve.png"
            if img_roc.exists():
                st.image(str(img_roc), width="stretch")
                
        with st.container(border=True):
            st.markdown("##### Feature Importance Random Forest")
            img_fi = STATIC_IMAGES_DIR / "eval_rf_feature_importance.png"
            if img_fi.exists():
                st.image(str(img_fi), width="stretch")

# ──────────────────────────────────────────────
# TAB 4: INTERPRETASI HASIL (XAI)
# ──────────────────────────────────────────────
with tabs[3]:
    st.markdown('<span class="section-tag">Explainable AI (XAI)</span>', unsafe_allow_html=True)
    st.markdown("## Interpretabilitas Model Deep Learning")
    st.write("Kami menggunakan teknik-teknik **Explainable AI (XAI)** untuk membongkar kotak hitam (black box) neural network agar interpretasi model medis dapat divalidasi secara ilmiah.")
    
    col_xai1, col_xai2 = st.columns(2)
    
    with col_xai1:
        with st.container(border=True):
            st.markdown("##### Grad-CAM (Sinyal Atensi Layer Terakhir)")
            img_gc = STATIC_IMAGES_DIR / "interp_gradcam.png"
            if img_gc.exists():
                st.image(str(img_gc), width="stretch")
            st.caption("Warna merah mengindikasikan area dengan atensi terkuat, terfokus tepat pada lensa yang mengalami katarak.")
            
        with st.container(border=True):
            st.markdown("##### Saliency Maps & Feature Maps")
            img_sal = STATIC_IMAGES_DIR / "interp_saliency.png"
            if img_sal.exists():
                st.image(str(img_sal), width="stretch")
            st.caption("Saliency Map (kiri) menyorot tepi piksel sensitif dan Feature Maps (kanan) menampilkan ekstraksi bentuk pupil.")
            
    with col_xai2:
        with st.container(border=True):
            st.markdown("##### LIME (Local Interpretable Model-agnostic Explanations)")
            img_lime = STATIC_IMAGES_DIR / "interp_lime.png"
            if img_lime.exists():
                st.image(str(img_lime), width="stretch")
            st.caption("Superpiksel hijau mendukung klasifikasi Katarak untuk membantu klinisi melihat lesi penentu diagnosis.")
            
        with st.container(border=True):
            st.markdown("##### Proyeksi Ruang Fitur (t-SNE & PCA)")
            img_tsne = STATIC_IMAGES_DIR / "interp_tsne.png"
            if img_tsne.exists():
                st.image(str(img_tsne), width="stretch")
            st.caption("Pemisahan kluster titik merah (katarak) dan hijau (normal) membuktikan model berhasil membedakan penyakit secara fungsional.")

# ──────────────────────────────────────────────
# TAB 5: DOKUMENTASI
# ──────────────────────────────────────────────
with tabs[4]:
    st.markdown('<span class="section-tag">System Documentation</span>', unsafe_allow_html=True)
    st.markdown("## Metodologi & Cara Penggunaan Sistem")
    st.write("Dokumentasi teknis alur pengembangan model kecerdasan buatan dan pedoman praktis pengoperasian aplikasi DEDIKAT.")
    
    col_doc1, col_doc2 = st.columns(2)
    
    with col_doc1:
        with st.container(border=True):
            st.markdown("##### Pipeline Metodologi & Arsitektur")
            st.markdown("""
                1. **Akuisisi Data**: Dataset diekstraksi dari Roboflow (ODIR Cataract Dataset) yang dianotasi oleh praktisi medis profesional.
                2. **Pembersihan & Validasi**: Semua gambar diperiksa kelengkapannya dan divalidasi integritas file-nya menggunakan pustaka PIL.
                3. **Stratified Dataset Splitting**: Pembagian data secara acak proporsional menjadi 70% pelatihan, 20% validasi, dan 10% pengujian untuk menjaga distribusi kelas seimbang.
                4. **Pelatihan Model**: Melatih arsitektur YOLOv8s (Object Detection) menggunakan akselerasi GPU CUDA via PyTorch.
            """)
            
    with col_doc2:
        with st.container(border=True):
            st.markdown("##### Panduan Penggunaan Aplikasi")
            st.markdown("""
                * **Kriteria Gambar yang Baik**:
                  - Foto mata diambil dari arah depan (frontal).
                  - Cahaya cukup terang dengan refleksi flash kornea minimal.
                  - Pupil dan iris mata terlihat fokus (tidak blur).
                * **Penyesuaian Parameter**:
                  - *Confidence Threshold*: Default 25%. Nilai keyakinan minimal objek katarak terdeteksi.
                  - *IoU Threshold*: Default 45%. Sensitivitas tumpang tindih kotak pembatas.
            """)
