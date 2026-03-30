"""Uygulama genelinde kullanılan sabitler."""

APP_TITLE = "STEM Vision Assistant"
APP_DESCRIPTION = (
    "Teknik grafik yükleyin; Gemini grafiği kısa ve öz, öğretmen tonunda Türkçe özetler. "
    "Özet edge-tts ile seslendirilir. API anahtarı (.env) gerekir."
)

DEFAULT_GEMINI_MODEL = "gemini-1.5-flash"
GEMINI_REQUEST_TIMEOUT_SEC = 90.0

ALLOWED_IMAGE_TYPES = ("image/jpeg", "image/png", "image/webp")

# edge-tts Türkçe ses (ör. tr-TR-AhmetNeural); EDGE_TTS_VOICE ile .env üzerinden değiştirilebilir.
DEFAULT_EDGE_TTS_VOICE = "tr-TR-EmelNeural"
