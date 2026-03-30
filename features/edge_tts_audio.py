"""
Microsoft Edge TTS (edge-tts) ile metin → MP3 ve Streamlit ses oynatıcı.

Gemini Markdown çıktısı önce ekranda gösterilir; ses üretimi bu işin sonunda
çalışır ki API analizini geciktirmesin.
"""

from __future__ import annotations

import asyncio
import html
import os
import re
from typing import Optional

import streamlit as st

from edge_tts import Communicate
from edge_tts.communicate import remove_incompatible_characters

from constants import DEFAULT_EDGE_TTS_VOICE

# edge-tts servisi çok uzun metinlerde sorun çıkarabilir; güvenli üst sınır.
_MAX_TTS_CHARS = 6000


def strip_markdown_for_speech(markdown_text: str) -> str:
    """
    Seslendirme için Markdown sözdizimini kaldırır; düz Türkçe metin döner.

    Başlıklar, kalın yazı, bağlantılar ve kod parçaları sadeleştirilir.
    """
    if not markdown_text:
        return ""
    t = markdown_text
    t = re.sub(r"^#{1,6}\s+", "", t, flags=re.MULTILINE)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"`([^`]+)`", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


async def _synthesize_mp3_bytes(text: str, voice: str) -> bytes:
    """edge-tts akışından MP3 baytlarını toplar."""
    clean = remove_incompatible_characters(text)
    communicate = Communicate(clean, voice)
    chunks: list[bytes] = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            chunks.append(chunk["data"])
    return b"".join(chunks)


def synthesize_teacher_summary_mp3(
    plain_text: str,
    *,
    voice: Optional[str] = None,
    max_chars: int = _MAX_TTS_CHARS,
) -> bytes:
    """
    Düz metni MP3 ses verisine çevirir (senkron sarmalayıcı; içeride asyncio.run).

    Raises:
        RuntimeError: Ağ veya servis hatasında anlamlı Türkçe mesaj.
    """
    v = (voice or os.getenv("EDGE_TTS_VOICE") or DEFAULT_EDGE_TTS_VOICE).strip()
    t = (plain_text or "").strip()
    if not t:
        raise RuntimeError("Seslendirilecek metin boş.")
    if len(t) > max_chars:
        t = t[: max_chars - 20].rstrip() + "… Metnin tamamı ekranda."

    try:
        return asyncio.run(_synthesize_mp3_bytes(t, v))
    except Exception as exc:
        raise RuntimeError(
            "Seslendirme servisine bağlanılamadı. İnternet bağlantınızı kontrol edin."
        ) from exc


def audio_player_ekle(
    audio_mp3: bytes,
    *,
    aria_label: str = "Öğretmen özeti seslendirmesi",
    autoplay: bool = True,
) -> None:
    """
    Streamlit `st.audio` ile MP3 oynatır; otomatik oynatma için `autoplay=True`.

    Görme engelli kullanıcılar için kısa bir `aria-live` durumu eklenir.
    """
    if not audio_mp3:
        return
    safe = html.escape(aria_label)
    st.markdown(
        f'<p role="status" aria-live="polite" aria-atomic="true" '
        f'style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
        f"overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;\">{safe}</p>",
        unsafe_allow_html=True,
    )
    st.audio(audio_mp3, format="audio/mp3", autoplay=autoplay)


def sonifikasyon_son_adim(
    image_bytes: bytes,
    analysis_markdown: str,
) -> None:
    """
    İleride grafik verisinden doğrudan ses (ör. pitch, süre) üretilecekse buraya eklenir.

    Şu an boş: analiz ve TTS bittikten sonra çağrılır, akışı bloklamaz.
    """
    _ = (image_bytes, analysis_markdown)
    return
