import streamlit as st

def initialize_history():
    """Session State üzerinde geçmiş listesini ve görünüm modunu başlatır."""
    if "history" not in st.session_state:
        st.session_state.history = []
    if "history_view_active" not in st.session_state:
        st.session_state.history_view_active = False

def add_to_history(source_name, analysis_result, image_bytes):
    """Yeni analizi geçmişe ekler."""
    # Aynı analizi tekrar eklememek için kontrol
    if not any(h['name'] == source_name for h in st.session_state.history):
        st.session_state.history.insert(0, {
            "name": source_name,
            "result": analysis_result,
            "image": image_bytes
        })

def render_history_sidebar():
    """Sidebar'da geçmişi çizer ve tıklanan kaydı ana ekrana 'enjekte' eder."""
    st.header("📜 Geçmiş Analizler")
    
    if not st.session_state.history:
        st.info("Henüz analiz yapılmadı.")
        return

    # Geçmişi temizleme seçeneği
    if st.sidebar.button("🗑️ Tüm Geçmişi Temizle"):
        st.session_state.history = []
        st.session_state.history_view_active = False
        st.rerun()

    st.divider()

    for i, item in enumerate(st.session_state.history):
        if st.sidebar.button(f"📄 {item['name']}", key=f"hist_{i}", use_container_width=True):
            # KRİTİK: Ana kodun (app.py) kullandığı kutuları dolduruyoruz
            st.session_state.last_analysis = item['result']
            st.session_state.history_image = item['image']
            st.session_state.history_view_active = True # "Geçmişten bakıyoruz" sinyali
            st.rerun()