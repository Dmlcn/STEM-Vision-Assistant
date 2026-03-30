"""
Yüksek kontrast tema stilleri.

Az gören kullanıcılar ve düşük ekran parlaklığı için siyah zemin,
beyaz/sarı metin (user-flow.md ile uyumlu).
"""

HIGH_CONTRAST_CSS = """
<style>
    /* Ana sayfa zemin ve metin */
    .stApp {
        background-color: #0d0d0d !important;
        color: #f5f5f5 !important;
    }
    /* Başlık ve gövde metni */
    h1, h2, h3, .stMarkdown p, label {
        color: #f5f5f5 !important;
    }
    /* Vurgu: sarı — başlık altı bilgi */
    .accent-text {
        color: #ffeb3b !important;
        font-size: 1.05rem;
    }
    /* Sonuç bölgesi — ekran okuyucu için görsel çerçeve */
    #analysis-result-region {
        border: 2px solid #ffeb3b;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1rem;
        background-color: #1a1a1a;
    }
    /* Streamlit widget etiketleri */
    [data-testid="stWidgetLabel"] {
        color: #f5f5f5 !important;
    }
</style>
"""


def inject_high_contrast_theme() -> None:
    """Streamlit sayfasına yüksek kontrast CSS enjekte eder."""
    import streamlit as st

    st.markdown(HIGH_CONTRAST_CSS, unsafe_allow_html=True)
