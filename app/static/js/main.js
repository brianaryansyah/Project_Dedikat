/* ============================================================
   DEDIKAT — Main JavaScript
   Handles: Tab Switching, Upload, Detection, Lightbox, Slider, Print, UI
   ============================================================ */

// ──────────────────────────────────────
// DOM Elements
// ──────────────────────────────────────
const uploadArea      = document.getElementById('uploadArea');
const fileInput       = document.getElementById('fileInput');
const previewArea     = document.getElementById('previewArea');
const previewImg      = document.getElementById('previewImg');
const previewInfo     = document.getElementById('previewInfo');
const btnRemove       = document.getElementById('btnRemove');
const btnDetect       = document.getElementById('btnDetect');
const resultPanel     = document.getElementById('resultPanel');
const resultPlaceholder = document.getElementById('resultPlaceholder');
const resultContent   = document.getElementById('resultContent');
const loadingOverlay  = document.getElementById('loadingOverlay');
const toast           = document.getElementById('toast');
const toastMsg        = document.getElementById('toastMsg');
const confSlider      = document.getElementById('confSlider');
const confValue       = document.getElementById('confValue');
const iouSlider       = document.getElementById('iouSlider');
const iouValue        = document.getElementById('iouValue');
const settingsToggle  = document.getElementById('settingsToggle');
const settingsContent = document.getElementById('settingsContent');
const navbar          = document.getElementById('navbar');
const btnReset        = document.getElementById('btnReset');
const btnDownload     = document.getElementById('btnDownload');

// Tab & Lightbox Elements
const tabs            = document.querySelectorAll('.nav-tab');
const tabPanes        = document.querySelectorAll('.tab-pane');
const lightbox        = document.getElementById('lightbox');
const lightboxImg     = document.getElementById('lightboxImg');
const lightboxClose   = document.getElementById('lightboxClose');
const lightboxCaption = document.getElementById('lightboxCaption');

// Slider & View Mode Elements
const btnViewSlider       = document.getElementById('btnViewSlider');
const btnViewSide         = document.getElementById('btnViewSide');
const sliderViewContainer = document.getElementById('sliderViewContainer');
const sideViewContainer   = document.getElementById('sideViewContainer');
const viewModeToggle      = document.getElementById('viewModeToggle');

const sliderHandle        = document.getElementById('sliderHandle');
const afterImageContainer = document.getElementById('afterImageContainer');
const sliderDivider       = document.getElementById('sliderDivider');
const sliderOriginalImg   = document.getElementById('sliderOriginalImg');
const sliderDetectionImg  = document.getElementById('sliderDetectionImg');

// Print Elements
const btnPrintReport = document.getElementById('btnPrintReport');

// Clinical Sample Buttons
const sampleCataractBtn = document.getElementById('sampleCataractBtn');
const sampleNormalBtn   = document.getElementById('sampleNormalBtn');

// Scanning line elements
const scanOverlay = document.getElementById('scanOverlay');
const loadingProgressText = document.getElementById('loadingProgressText');

// ──────────────────────────────────────
// State
// ──────────────────────────────────────
let selectedFile = null;
let lastResult   = null;
let progressInterval = null;

// ──────────────────────────────────────
// Fetch GPU Status on Load
// ──────────────────────────────────────
async function checkSystemStatus() {
    const gpuNameEl = document.getElementById('sysGpuName');
    try {
        const res = await fetch('/status');
        if (res.ok) {
            const data = await res.json();
            if (data.gpu_available) {
                gpuNameEl.textContent = data.gpu_name || 'NVIDIA GPU';
                gpuNameEl.className = 'monitor-value badge-glow';
            } else {
                gpuNameEl.textContent = 'CPU Mode';
                gpuNameEl.className = 'monitor-value';
                gpuNameEl.style.color = 'var(--text-secondary)';
            }
        }
    } catch (e) {
        console.error('Gagal memuat status GPU:', e);
        gpuNameEl.textContent = 'CPU Mode';
    }
}
checkSystemStatus();

// ──────────────────────────────────────
// Navbar Scroll Effect
// ──────────────────────────────────────
window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ──────────────────────────────────────
// Tab Navigasi Switching
// ──────────────────────────────────────
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const targetTab = tab.getAttribute('data-tab');
        
        // Ganti Tab Aktif di Navigasi
        tabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        
        // Tampilkan/Sembunyikan Konten Tab
        tabPanes.forEach(pane => {
            if (pane.id === `tab-${targetTab}`) {
                pane.classList.add('active');
            } else {
                pane.classList.remove('active');
            }
        });
        
        // Scroll ke atas halaman
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});

// ──────────────────────────────────────
// Lightbox (Klik Perbesar Gambar Medis)
// ──────────────────────────────────────
document.addEventListener('click', e => {
    if (e.target.classList.contains('clickable-img')) {
        lightboxImg.src = e.target.src;
        lightboxCaption.textContent = e.target.alt || 'Visualisasi Analisis DEDIKAT';
        lightbox.style.display = 'flex';
    }
});

lightboxClose.addEventListener('click', () => {
    lightbox.style.display = 'none';
});

lightbox.addEventListener('click', e => {
    if (e.target === lightbox) {
        lightbox.style.display = 'none';
    }
});

// ──────────────────────────────────────
// Before/After Slider Drag Handling
// ──────────────────────────────────────
if (sliderHandle && afterImageContainer && sliderDivider) {
    sliderHandle.addEventListener('input', (e) => {
        const val = e.target.value;
        afterImageContainer.style.clipPath = `polygon(0 0, ${val}% 0, ${val}% 100%, 0 100%)`;
        sliderDivider.style.left = `${val}%`;
    });
}

// View Mode Toggles
if (btnViewSlider && btnViewSide && sliderViewContainer && sideViewContainer) {
    btnViewSlider.addEventListener('click', () => {
        btnViewSlider.classList.add('active');
        btnViewSide.classList.remove('active');
        sliderViewContainer.style.display = 'block';
        sideViewContainer.style.display = 'none';
    });

    btnViewSide.addEventListener('click', () => {
        btnViewSide.classList.add('active');
        btnViewSlider.classList.remove('active');
        sideViewContainer.style.display = 'block';
        sliderViewContainer.style.display = 'none';
    });
}

// ──────────────────────────────────────
// Print Medical Report
// ──────────────────────────────────────
if (btnPrintReport) {
    btnPrintReport.addEventListener('click', () => {
        if (!lastResult) {
            showToast('Tidak ada hasil analisis untuk dicetak.');
            return;
        }
        window.print();
    });
}

// ──────────────────────────────────────
// Toast Notification (Emoji Removed)
// ──────────────────────────────────────
function showToast(message, duration = 3000) {
    toastMsg.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

// ──────────────────────────────────────
// Quick Test Sample Image Loader
// ──────────────────────────────────────
async function loadSampleImage(filename, displayName) {
    try {
        // Show loading progress
        setDetecting(true, true);
        const response = await fetch(`/static/images/samples/${filename}`);
        if (!response.ok) throw new Error('Network response not ok');
        const blob = await response.blob();
        const file = new File([blob], filename, { type: 'image/jpeg' });
        
        setDetecting(false);
        handleFile(file);
        showToast(`Berhasil memuat ${displayName}`);
    } catch (e) {
        setDetecting(false);
        console.error('Gagal memuat gambar sampel:', e);
        showToast('Gagal memuat gambar sampel.');
    }
}

if (sampleCataractBtn) {
    sampleCataractBtn.addEventListener('click', () => {
        loadSampleImage('cataract_sample.jpg', 'Sampel Lensa Katarak');
    });
}
if (sampleNormalBtn) {
    sampleNormalBtn.addEventListener('click', () => {
        loadSampleImage('normal_sample.jpg', 'Sampel Lensa Normal');
    });
}

// ──────────────────────────────────────
// File Upload & Input
// ──────────────────────────────────────
uploadArea.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', e => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

// Drag & Drop
uploadArea.addEventListener('dragover', e => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', e => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) handleFile(files[0]);
});

// Handle File
function handleFile(file) {
    const allowed = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/bmp'];
    if (!allowed.includes(file.type)) {
        showToast('Format file tidak didukung. Gunakan JPG, PNG, WEBP, atau BMP.');
        return;
    }

    if (file.size > 16 * 1024 * 1024) {
        showToast('File terlalu besar. Maksimal ukuran 16MB.');
        return;
    }

    selectedFile = file;

    const reader = new FileReader();
    reader.onload = e => {
        previewImg.src = e.target.result;
        uploadArea.style.display = 'none';
        previewArea.style.display = 'block';

        const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
        previewInfo.textContent = `${file.name} — ${sizeMB} MB`;

        btnDetect.disabled = false;
        showToast('Gambar berhasil terpilih!');
        showPlaceholder();
    };
    reader.readAsDataURL(file);
}

// Remove File
btnRemove.addEventListener('click', (e) => {
    e.stopPropagation();
    resetUpload();
});

function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    previewImg.src = '';
    previewArea.style.display = 'none';
    uploadArea.style.display = 'flex';
    btnDetect.disabled = true;
    showPlaceholder();
}

// ──────────────────────────────────────
// Konfigurasi Ambang Batas (Sliders)
// ──────────────────────────────────────
settingsToggle.addEventListener('click', () => {
    settingsContent.classList.toggle('open');
    settingsToggle.querySelector('.toggle-icon').classList.toggle('open');
});

confSlider.addEventListener('input', () => {
    confValue.textContent = confSlider.value + '%';
});

iouSlider.addEventListener('input', () => {
    iouValue.textContent = iouSlider.value + '%';
});

// ──────────────────────────────────────
// Stat Numbers Animation
// ──────────────────────────────────────
function animateNumber(element, start, end, duration, suffix = "") {
    if (!element) return;
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const currentVal = Math.floor(progress * (end - start) + start);
        element.textContent = currentVal + suffix;
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            element.textContent = end + suffix;
        }
    };
    window.requestAnimationFrame(step);
}

// ──────────────────────────────────────
// Deteksi — Main Function
// ──────────────────────────────────────
btnDetect.addEventListener('click', async () => {
    if (!selectedFile) {
        showToast('Pilih gambar terlebih dahulu!');
        return;
    }

    setDetecting(true);

    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('conf', confSlider.value / 100);
        formData.append('iou', iouSlider.value / 100);

        const response = await fetch('/detect', {
            method: 'POST',
            body: formData,
        });

        if (!response.ok) {
            throw new Error(`HTTP error ${response.status}`);
        }

        const data = await response.json();
        
        setDetecting(false);

        if (data.success) {
            lastResult = data;
            displayResult(data);
        } else {
            showToast(data.error || 'Terjadi kesalahan');
            showPlaceholder();
        }

    } catch (err) {
        setDetecting(false);
        console.error('Detection error:', err);
        showToast('Gagal terhubung ke server. Pastikan Flask berjalan.');
        showPlaceholder();
    }
});

// Set Detecting State & Interactive Scanning Phrases
function setDetecting(loading, isSampleLoad = false) {
    if (loading) {
        loadingOverlay.style.display = 'flex';
        btnDetect.disabled = true;
        btnDetect.querySelector('.btn-text').style.display = 'none';
        btnDetect.querySelector('.btn-spinner').style.display = 'block';
        if (scanOverlay) scanOverlay.style.display = 'block';

        // Dynamic progress scanning bar sentences
        const scanPhrases = isSampleLoad ? [
            "Mengunduh Citra Sampel...",
            "Memuat Aset Medis...",
            "Inisialisasi Preview..."
        ] : [
            "Menyusun Citra & Fokus Pupil...",
            "Menyeimbangkan Kontras Citra...",
            "Melakukan Segmentasi Lensa Pupil...",
            "Ekstraksi Fitur Patologis Lensa...",
            "Menjalankan Model Deteksi YOLOv8s...",
            "Menyelesaikan Bounding Box..."
        ];

        let index = 0;
        loadingProgressText.textContent = scanPhrases[0];
        
        if (progressInterval) clearInterval(progressInterval);
        progressInterval = setInterval(() => {
            index = (index + 1) % scanPhrases.length;
            loadingProgressText.textContent = scanPhrases[index];
        }, 500);

    } else {
        loadingOverlay.style.display = 'none';
        btnDetect.disabled = false;
        btnDetect.querySelector('.btn-text').style.display = 'block';
        btnDetect.querySelector('.btn-spinner').style.display = 'none';
        if (scanOverlay) scanOverlay.style.display = 'none';
        
        if (progressInterval) {
            clearInterval(progressInterval);
            progressInterval = null;
        }
    }
}

// Display Result (Emojis Removed)
function displayResult(data) {
    resultPlaceholder.style.display = 'none';
    resultContent.style.display    = 'flex';

    // Status utama
    const statusEl  = document.getElementById('resultStatus');
    const statusIcon = document.getElementById('statusIconLarge');
    const statusTitle = document.getElementById('statusTitle');
    const statusDesc  = document.getElementById('statusDesc');

    if (data.overall_status === 'normal') {
        statusEl.style.background    = 'rgba(16, 185, 129, 0.08)';
        statusEl.style.borderColor   = 'rgba(16, 185, 129, 0.25)';
        // Clean checkmark SVG
        statusIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-success)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        statusTitle.textContent      = data.status_text;
        statusTitle.style.color      = 'var(--color-success)';
    } else {
        statusEl.style.background    = 'rgba(239, 68, 68, 0.08)';
        statusEl.style.borderColor   = 'rgba(239, 68, 68, 0.25)';
        // Clean warning alert SVG
        statusIcon.innerHTML = `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-danger)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`;
        statusTitle.textContent      = data.status_text;
        statusTitle.style.color      = 'var(--color-danger)';
    }
    statusDesc.textContent = data.status_desc;

    // Load Side-by-side Images
    const originalImg   = document.getElementById('originalImg');
    const detectionImg  = document.getElementById('detectionImg');
    if (data.original_image_url) originalImg.src = data.original_image_url;
    if (data.result_image) detectionImg.src = 'data:image/jpeg;base64,' + data.result_image;

    // Load Slider Images
    if (data.original_image_url) sliderOriginalImg.src = data.original_image_url;
    if (data.result_image) sliderDetectionImg.src = 'data:image/jpeg;base64,' + data.result_image;
    
    // Reset Slider states to 50% split
    sliderHandle.value = 50;
    afterImageContainer.style.clipPath = `polygon(0 0, 50% 0, 50% 100%, 0 100%)`;
    sliderDivider.style.left = `50%`;
    viewModeToggle.style.display = 'flex';

    // Stats countup animations
    animateNumber(document.getElementById('numDetections'), 0, data.num_detections, 1000);
    animateNumber(document.getElementById('inferenceTime'), 0, Math.round(data.inference_time), 800);
    const deviceText = data.device_used || 'CPU';
    document.getElementById('deviceUsed').textContent = deviceText.includes('GPU') ? 'GPU CUDA' : 'CPU';

    // Populate Detections List
    const listEl = document.getElementById('detectionList');
    listEl.innerHTML = '';

    if (data.detections && data.detections.length > 0) {
        const header = document.createElement('div');
        header.style.cssText = 'font-size:0.82rem;font-weight:700;color:var(--text-muted);margin-bottom:4px;text-transform:uppercase;letter-spacing:0.05em;';
        header.textContent = `Rincian Temuan AI (${data.detections.length} objek)`;
        listEl.appendChild(header);

        data.detections.forEach((det, i) => {
            const item = document.createElement('div');
            item.className = 'detection-item fade-in';
            item.style.animationDelay = `${i * 60}ms`;

            const confColor = det.confidence >= 80 ? 'var(--color-danger)' : 
                              det.confidence >= 50 ? 'var(--color-warning)' : 'var(--color-info)';

            item.innerHTML = `
                <div class="det-info">
                    <div class="det-class" style="color:${confColor}">${det.class_name}</div>
                    <div class="det-bbox">BBox: [${det.bbox.join(', ')}]</div>
                </div>
                <div class="det-right">
                    <span class="det-conf-text" style="color:${confColor}">${det.confidence}%</span>
                    <div class="conf-bar-wrap">
                        <div class="conf-bar" style="width:${det.confidence}%;background:${confColor}"></div>
                    </div>
                    <span class="severity-badge" style="background:${det.sev_color}18;color:${det.sev_color};border:1px solid ${det.sev_color}33;">
                        Keyakinan ${det.severity}
                    </span>
                </div>
            `;
            listEl.appendChild(item);
        });
    }

    // Rekomendasi (Emojis Removed)
    const recEl = document.getElementById('recommendation');
    if (data.overall_status === 'normal') {
        recEl.style.background    = 'rgba(16, 185, 129, 0.05)';
        recEl.style.borderColor   = 'rgba(16, 185, 129, 0.2)';
        recEl.style.color         = '#065f46';
        recEl.innerHTML = `
            <strong>Rekomendasi DEDIKAT:</strong><br>
            Analisis kecerdasan buatan menunjukkan kondisi lensa mata Anda normal dan jernih tanpa tanda katarak. Disarankan untuk tetap menjaga kebiasaan hidup sehat dan melakukan pemeriksaan mata secara berkala ke dokter spesialis minimal 1 tahun sekali.
        `;
    } else {
        recEl.style.background    = 'rgba(239, 68, 68, 0.05)';
        recEl.style.borderColor   = 'rgba(239, 68, 68, 0.2)';
        recEl.style.color         = '#991b1b';
        recEl.innerHTML = `
            <strong>Rekomendasi Medis DEDIKAT:</strong><br>
            Terdeteksi indikasi kelainan lensa mata (katarak). Segera jadwalkan konsultasi dengan dokter spesialis mata (Sp.M) untuk pemeriksaan lampu celah (slit-lamp exam) guna diagnosis definitif. Deteksi dini meningkatkan keberhasilan terapi pemulihan penglihatan secara optimal.
        `;
    }

    // Populate Print Report Template
    document.getElementById('printReportId').textContent = 'DK-' + Math.floor(Math.random() * 900000 + 100000);
    const now = new Date();
    const formattedDate = now.toLocaleDateString('id-ID', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('printReportDate').textContent = formattedDate;
    document.getElementById('printReportDevice').textContent = deviceText.includes('GPU') ? 'GPU CUDA' : 'CPU';
    document.getElementById('printImgOriginal').src = data.original_image_url;
    document.getElementById('printImgDetection').src = 'data:image/jpeg;base64,' + data.result_image;
    document.getElementById('printReportStatus').textContent = data.overall_status === 'normal' ? 'TIDAK TERDETEKSI KATARAK' : 'TERDETEKSI KATARAK (POSITIF)';
    document.getElementById('printReportStatus').style.color = data.overall_status === 'normal' ? '#10b981' : '#ef4444';
    document.getElementById('printReportCount').textContent = data.num_detections + ' Objek';
    document.getElementById('printReportTime').textContent = Math.round(data.inference_time) + ' ms';
    document.getElementById('printReportConf').textContent = confSlider.value + '%';

    const printList = document.getElementById('printReportDetectionsList');
    printList.innerHTML = '';
    if (data.detections && data.detections.length > 0) {
        data.detections.forEach(det => {
            const item = document.createElement('p');
            item.style.margin = '4px 0';
            item.innerHTML = `• <strong>${det.class_name}</strong> - Keyakinan: ${det.confidence}% (Severity: ${det.severity}) - Bounding Box: [${det.bbox.join(', ')}]`;
            printList.appendChild(item);
        });
    } else {
        const item = document.createElement('p');
        item.textContent = 'Tidak ada objek katarak terdeteksi pada pupil.';
        printList.appendChild(item);
    }

    const printRec = document.getElementById('printReportRecommendation');
    if (data.overall_status === 'normal') {
        printRec.innerHTML = `<strong>Rekomendasi Skrining Cerdas (Negatif Katarak):</strong> Lensa mata terlihat normal. Tetap jaga pola makan kaya antioksidan dan periksakan mata Anda ke dokter spesialis secara berkala minimal 1 tahun sekali.`;
    } else {
        printRec.innerHTML = `<strong>Rekomendasi Skrining Cerdas (Positif Katarak):</strong> Terdeteksi adanya kekeruhan patologis pada lensa. Pasien sangat disarankan untuk segera melakukan pemeriksaan slit-lamp ke dokter spesialis mata (Sp.M) untuk diagnosis definitif dan perencanaan tindakan bedah fakoemulsifikasi jika diperlukan.`;
    }

    // Scroll ke panel hasil
    resultPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    showToast('Analisis selesai!');
}

function showPlaceholder() {
    resultPlaceholder.style.display = 'flex';
    resultContent.style.display    = 'none';
    viewModeToggle.style.display   = 'none';
}

// Reset Button
btnReset.addEventListener('click', () => {
    resetUpload();
    lastResult = null;
    showToast('Sistem siap menerima pengujian citra baru.');
});

// Download Result
btnDownload.addEventListener('click', () => {
    if (!lastResult || !lastResult.result_image) {
        showToast('Tidak ada hasil analisis untuk disimpan.');
        return;
    }

    const link = document.createElement('a');
    link.href  = 'data:image/jpeg;base64,' + lastResult.result_image;
    link.download = `dedikat_analisis_${Date.now()}.jpg`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    showToast('Hasil analisis berhasil diunduh!');
});

// ──────────────────────────────────────
// Scroll Animation Observer (Premium Feel)
// ──────────────────────────────────────
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.05 });

document.querySelectorAll('.visual-card, .docs-section-card, .upload-panel, .result-panel, .system-monitor-card, .business-insights-panel').forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(25px)';
    el.style.transition = `opacity 0.45s ease ${i * 50}ms, transform 0.45s ease ${i * 50}ms`;
    observer.observe(el);
});

// ──────────────────────────────────────
// Init Info (Emojis Cleaned)
// ──────────────────────────────────────
console.log('%c DEDIKAT — Deteksi Dini Katarak', 
    'color:#00ABE4;font-size:1.1rem;font-weight:bold;');
console.log('%c Academic ML Project - Universitas Dian Nuswantoro', 
    'color:#475569;font-size:0.82rem;');
