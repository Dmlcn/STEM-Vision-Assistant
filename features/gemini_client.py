"""
Gemini Vision: Grafik analizi için ana istemci dosyası.
"""

from __future__ import annotations
import os
from io import BytesIO
from typing import Any, Optional
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions
from google.generativeai.types import RequestOptions
from PIL import Image

# Sabitleri ve Promptları içeri aktar
from constants import DEFAULT_GEMINI_MODEL, GEMINI_REQUEST_TIMEOUT_SEC
from prompts import TEACHER_NARRATIVE_SYSTEM, TEACHER_NARRATIVE_USER

class GeminiAnalysisError(Exception):
    """Kullanıcıya gösterilecek hata mesajlarını yöneten sınıf."""
    def __init__(self, user_message: str) -> None:
        self.user_message = user_message
        super().__init__(user_message)

def _resolve_model_name(explicit: Optional[str]) -> str:
    if explicit and explicit.strip():
        return explicit.strip()
    return (os.getenv("GEMINI_MODEL") or DEFAULT_GEMINI_MODEL).strip()

def _extract_response_text(response: Any) -> str:
    """Modelden gelen yanıtı güvenli bir şekilde metne dönüştürür."""
    try:
        if hasattr(response, "text") and response.text:
            return str(response.text)
    except ValueError:
        pass
    return "Yanıt alınamadı."

def analyze_graph_teacher_narrative(
    image_bytes: bytes,
    *,
    api_key: str,
    model_name: Optional[str] = None,
) -> str:
    """Grafiği analiz eder ve metin olarak döndürür."""
    key = (api_key or "").strip()
    if not key:
        raise GeminiAnalysisError("API anahtarı eksik.")

    genai.configure(api_key=key)
    model = genai.GenerativeModel(
        _resolve_model_name(model_name),
        system_instruction=TEACHER_NARRATIVE_SYSTEM,
    )

    try:
        pil_image = Image.open(BytesIO(image_bytes))
        pil_image.load()
        
        response = model.generate_content(
            [TEACHER_NARRATIVE_USER, pil_image],
            request_options=RequestOptions(timeout=60),
        )
        return _extract_response_text(response).strip()
        
    except google_exceptions.GoogleAPIError as err:
        raise GeminiAnalysisError(f"API Hatası: {str(err)[:100]}")
    except Exception as e:
        raise GeminiAnalysisError(f"Beklenmedik hata: {e}")