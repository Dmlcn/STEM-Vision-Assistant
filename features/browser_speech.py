"""
Tarayıcı konuşması (Web Speech API).

- Analiz başlarken ve sonuç gelince **otomatik** seslendirme
- «Metni seslendir» ile **manuel** tekrar
"""

from __future__ import annotations

import html
import json

import streamlit as st
import streamlit.components.v1 as components

WAITING_MESSAGE_TR = "Analiz motoru çalışıyor, lütfen bekleyiniz."
COMPLETE_SHORT_TR = "Analiz tamamlandı. Özet seslendirmesi aşağıda."


def _speech_synthesis_js(msg_json: str) -> str:
    return f"""
<script>
(function() {{
  const msg = {msg_json};
  try {{
    if (window.speechSynthesis) {{
      window.speechSynthesis.cancel();
      const u = new SpeechSynthesisUtterance(msg);
      u.lang = 'tr-TR';
      u.rate = 1.0;
      window.speechSynthesis.speak(u);
    }}
  }} catch (e) {{}}
}})();
</script>
"""


def announce_analysis_waiting() -> None:
    """Analiz başladığında otomatik: ekran okuyucu + konuşma (bekleme mesajı)."""
    safe = html.escape(WAITING_MESSAGE_TR)
    st.markdown(
        f'<p role="status" aria-live="assertive" aria-atomic="true" '
        f'style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
        f"overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;\">{safe}</p>",
        unsafe_allow_html=True,
    )
    msg_json = json.dumps(WAITING_MESSAGE_TR, ensure_ascii=False)
    components.html(_speech_synthesis_js(msg_json), height=1)


def announce_analysis_complete_short() -> None:
    """Gemini bittiğinde kısa durum; uzun metin edge-tts ile ayrı oynatılır."""
    safe = html.escape(COMPLETE_SHORT_TR)
    st.markdown(
        f'<p role="status" aria-live="assertive" aria-atomic="true" '
        f'style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
        f"overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;\">{safe}</p>",
        unsafe_allow_html=True,
    )


def announce_result_automatic(text: str, *, max_chars: int = 1600) -> None:
    """
    Analiz metni hazır olduğunda otomatik seslendirir (kısaltılmış uzun metin).

    Ekran okuyucu için assertive bölge + speechSynthesis.
    """
    t = (text or "").strip()
    if not t:
        return
    if len(t) > max_chars:
        t = t[: max_chars - 1].rstrip() + "… Kalan metin ekranda."

    safe = html.escape(t)
    st.markdown(
        f'<p role="status" aria-live="assertive" aria-atomic="true" '
        f'style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;'
        f"overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0;\">{safe}</p>",
        unsafe_allow_html=True,
    )
    msg_json = json.dumps(t, ensure_ascii=False)
    components.html(_speech_synthesis_js(msg_json), height=1)


def speak_text_on_demand(text: str, *, max_chars: int = 4000) -> None:
    """
    Kullanıcı düğmesiyle metni seslendirir (tekrar dinleme vb.).
    """
    t = (text or "").strip()
    if not t:
        return
    if len(t) > max_chars:
        t = t[: max_chars - 1].rstrip() + "…"

    msg_json = json.dumps(t, ensure_ascii=False)
    components.html(_speech_synthesis_js(msg_json), height=1)
