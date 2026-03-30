from __future__ import annotations
import streamlit as st
import os                           # Sisteme erişmek için (Hatanın kesin çözümü)
import hashlib                      # Görsellerin parmak izini almak için
from datetime import datetime       # Zaman damgası oluşturmak için
import streamlit.components.v1 as components
from dotenv import load_dotenv

# --- Kendi Modüllerimizden Importlar ---
# --- Kendi Modüllerimizden Importlar ---
from history_manager import initialize_history, add_to_history, render_history_sidebar
from browser_speech import (
    announce_analysis_complete_short,
    announce_analysis_waiting,
    speak_text_on_demand,
)
from edge_tts_audio import (
    audio_player_ekle,
    strip_markdown_for_speech,
    synthesize_teacher_summary_mp3,
)
from constants import APP_DESCRIPTION, APP_TITLE
from gemini_client import GeminiAnalysisError, analyze_graph_teacher_narrative
from theme import inject_high_contrast_theme

def _gemini_api_key():
    load_dotenv()
    for name in ("GEMINI_API_KEY", "GOOGLE_API_KEY"):
        k = (os.getenv(name) or "").strip()
        if k: return k
    return None
   
def play_notification_sound(sound_type="start"):
    """Tarayıcıda anlık bildirim tonları çalar (Düzeltilmiş ve Resume eklenmiş)."""
    # Anahtarları ve sesleri netleştirdik
    tones = {
        "start": "[440, 0.1]",              # Başlatma: İnce bir 'tık'
        "success": "[523, 0.1, 659, 0.2]",  # Başarı: Pozitif çift ton
        "error": "[220, 0.3]"               # Hata: Kalın uyarı tonu
    }
    
    # Varsayılan olarak 'start' tonunu seçiyoruz
    tone_data = tones.get(sound_type, tones["start"])
    
    components.html(
        f"""
        <script>
        const context = new (window.AudioContext || window.webkitAudioContext)();
        
        async function playTone(freq, duration, start) {{
            // Tarayıcı engeli varsa sesi uyandır (Resume)
            if (context.state === 'suspended') {{
                await context.resume();
            }}
            
            const osc = context.createOscillator();
            const gain = context.createGain();
            osc.connect(gain);
            gain.connect(context.destination);
            osc.frequency.value = freq;
            gain.gain.setValueAtTime(0.1, context.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.0001, context.currentTime + duration);
            osc.start(context.currentTime + start);
            osc.stop(context.currentTime + start + duration);
        }}
        
        const data = {tone_data};
        for(let i=0; i < data.length; i+=2) {{
            playTone(data[i], data[i+1], i*0.1);
        }}
        </script>
        """,
        height=0
    )

def main():
    # 1. Uygulama Ayarları ve Temizlik
    st.set_page_config(page_title=APP_TITLE, page_icon="📊", layout="centered")
    inject_high_contrast_theme()
    
    # --- TASARIM: Akademik Rapor Görünümü (CSS) ---
    st.markdown("""
    <style>
        /* 1. Sürükle-Bırak Alanı (Vurgulu Kenarlık) */
        [data-testid="stFileUploader"] {
            border: 2px dashed #ff8c00 !important;
            border-radius: 10px;
            padding: 20px;
            background-color: #1a1a1a;
        }
        
        /* 2. Akademik Rapor Kartı (Turuncu Şeritli) */
        .report-card {
            background-color: #1e1e1e;
            border-left: 10px solid #ff8c00;
            border-radius: 12px;
            padding: 25px;
            margin-top: 25px;
            color: #ffffff;
            font-size: 18px;
            font-family: 'Segoe UI', sans-serif;
            line-height: 1.8;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }

        /* 3. Butonları Daha Belirgin Yap (Erişilebilirlik) */
        .stButton>button {
            border-radius: 8px !important;
            font-weight: bold !important;
            text-transform: uppercase;
        }
    </style>
    """, unsafe_allow_html=True)
    
    initialize_history()

    # 2. Yan Menü (Erişilebilir Geçmiş)
    with st.sidebar:
        render_history_sidebar()

    # 3. Ana Sayfa Başlıkları ve Kısayol Rehberi
    api_key = _gemini_api_key()
    st.title(APP_TITLE)
    
    # Tasarım: Kısayol Bilgi Paneli
    st.info("""
    💡 **Hızlı Kullanım Rehberi:**
    - **U**: Grafik Yükle | **Ctrl + Enter**: Analizi Başlat 
    - **S**: Sesi Durdur/Başlat | **R**: Sesi Başa Sar
    """, icon="⌨️")

    st.markdown(f'<p class="accent-text">{APP_DESCRIPTION}</p>', unsafe_allow_html=True)

    if not api_key:
        st.warning("🔑 API anahtarı eksik! Lütfen .env dosyasını kontrol edin.")

    # 4. Görsel Yükleme Alanı
    st.markdown("### 📸 Grafik Yükleyin")
    
    # Tasarım: Görseli Temizleme Butonu
    if st.session_state.get("last_image_hash"): # current_image yerine hash kontrolü
        if st.button("🗑️ Görseli Kaldır ve Sıfırla"):
            st.session_state.last_image_hash = None
            st.session_state.last_analysis = None
            st.session_state.tts_mp3 = None
            st.rerun()

    # --- 4. Görsel Yükleme ve Akıllı Kaynak Yönetimi ---
    image_bytes = None
    source_name = "Kamera"

    col_cam, col_file = st.columns(2)
    with col_cam:
        camera = st.camera_input("📸 Kamera Kullan")
    with col_file:
        uploaded = st.file_uploader("📁 Dosyadan Seç", type=["jpg", "jpeg", "png", "webp"])

    # Öncelik: Önce kameraya bak, yoksa dosyaya bak
    if camera:
        image_bytes = camera.getvalue()
        source_name = f"Kamera_{datetime.now().strftime('%H%M%S')}"
        st.session_state.history_view_active = False # Yeni giriş varsa geçmiş modunu kapat
    elif uploaded:
        image_bytes = uploaded.getvalue()
        source_name = uploaded.name
        st.session_state.history_view_active = False # Yeni giriş varsa geçmiş modunu kapat
    # İŞTE EKLEMEN GEREKEN KÖPRÜ:
    elif st.session_state.get("history_view_active"):
        image_bytes = st.session_state.history_image
        source_name = "Geçmiş Kayıt"

    # --- BUG FIX: Görsel Değiştiğinde Eski Veriyi Temizle ---
    if image_bytes:
        new_hash = hashlib.md5(image_bytes).hexdigest()
        if st.session_state.get("last_image_hash") != new_hash:
            # Yeni bir görsel algılandı, eski analizi ve sesi sıfırla
            st.session_state.last_analysis = None
            st.session_state.tts_mp3 = None
            st.session_state.last_image_hash = new_hash
    else:
        st.session_state.last_image_hash = None

    # --- 5. Analiz Süreci ---
    if image_bytes:
        st.image(image_bytes, caption="İşlenecek Teknik Grafik", use_container_width=True)
        
        analyze = st.button(
            "🚀 Analizi Başlat", 
            type="primary", 
            use_container_width=True,
            key="btn_analizi_baslat"
        )

        if analyze and api_key:
            # Kullanıcıya işlemin başladığını duyur
            announce_analysis_waiting() 
            
            try:
                with st.spinner("Gemini teknik grafiği inceliyor..."):
                    result = analyze_graph_teacher_narrative(image_bytes, api_key=api_key)
                    
                    # KRİTİK: Hata Kontrolü ve Sesli Geri Bildirim
                    if result.startswith("HATA"):
                        play_notification_sound("error")
                        st.error(result)
                        # Hatayı tarayıcı üzerinden sesli oku
                        components.html(f"""<script>
                            const msg = new SpeechSynthesisUtterance("{result}");
                            msg.lang = "tr-TR"; window.speechSynthesis.speak(msg);
                        </script>""", height=0)
                    else:
                        # Başarı Durumu
                        play_notification_sound("success")
                        st.session_state.last_analysis = result
                        st.session_state.tts_mp3 = None 
                        add_to_history(source_name, result, image_bytes)
                        announce_analysis_complete_short()
                        
            except Exception as e:
                play_notification_sound("error")
                st.error(f"Sistem Hatası: {e}")
                
                
    # 6. Sonuç Gösterimi ve Tasarım
    if st.session_state.get("last_analysis") and image_bytes:
        st.markdown('<div id="result_area" tabindex="-1"></div>', unsafe_allow_html=True)
        
        components.html(
            """
            <script>
                var resultArea = window.parent.document.getElementById("result_area");
                if (resultArea) {
                    resultArea.scrollIntoView({behavior: "smooth"});
                    resultArea.focus();
                }
            </script>
            """,
            height=0
        )

        st.divider()
        st.markdown("### 📝 Analiz Sonucu")
        
        # Tasarım: Akademik Rapor Kartı Uygulaması
        st.markdown(f'<div class="report-card">{st.session_state.last_analysis}</div>', unsafe_allow_html=True)

        # Otomatik Seslendirme
        if st.session_state.get("tts_mp3") is None:
            try:
                with st.spinner("Ses hazırlanıyor..."):
                    plain_text = strip_markdown_for_speech(st.session_state.last_analysis)
                    mp3_data = synthesize_teacher_summary_mp3(plain_text)
                    st.session_state.tts_mp3 = mp3_data
                    audio_player_ekle(mp3_data)
            except:
                st.warning("🔊 Seslendirme şu an yapılamıyor.")
        else:
            audio_player_ekle(st.session_state.tts_mp3)

        if st.button("🗣️ Sesli Analizi Baştan Başlat", help="Analizi en baştan dinlemek için tıklayın (Kısayol: R)"):
            components.html("<script>window.parent.document.querySelector('audio').currentTime = 0; window.parent.document.querySelector('audio').play();</script>", height=0)

   # --- 7. GELİŞMİŞ KISAYOL SİSTEMİ (Onarılmış Sürüm) ---
    components.html(
        """
        <script>
        const doc = window.parent.document;
        doc.addEventListener('keydown', function(e) {
            // Ctrl + Enter: Analizi Başlat
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault(); 
                e.stopPropagation();
                // Streamlit'te 'primary' buton genellikle bizim analiz butonumuzdur
                const btn = Array.from(doc.querySelectorAll('button')).find(el => 
                    el.innerText.includes('Analizi Başlat') || el.getAttribute('kind') === 'primary'
                );
                if (btn) btn.click();
            }
            // S Tuşu: Sesi Durdur/Başlat
            if (e.key.toLowerCase() === 's') {
                const audio = doc.querySelector('audio');
                if (audio) { if (audio.paused) audio.play(); else audio.pause(); }
            }
            // R Tuşu: Sesi Başa Sar
            if (e.key.toLowerCase() === 'r') {
                const audio = doc.querySelector('audio');
                if (audio) { audio.currentTime = 0; audio.play(); }
            }
            // U Tuşu: Grafik Yükle (Uploader'a Odaklan)
            if (e.key.toLowerCase() === 'u') {
                const fileInput = doc.querySelector('input[type="file"]');
                if (fileInput) fileInput.click();
            }
        }, true);
        </script>
        """,
        height=0,
    )

if __name__ == "__main__":
    main()