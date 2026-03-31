Tech Stack: STEM Vision Assistant
Bu döküman, projenin geliştirilmesinde kullanılan teknolojileri ve bu teknolojilerin seçilme nedenlerini açıklar.

1. Programlama Dili
Python (v3.10+): Yapay zeka ve veri bilimi ekosistemindeki geniş kütüphane desteği ve öğrenme kolaylığı nedeniyle ana dil olarak seçilmiştir.

JavaScript (ES6+): Tarayıcı tarafında düşük seviyeli klavye kısayolları ($keyboard$ $interceptors$) ve ses kontrolü sağlamak amacıyla kullanılmıştır.


2. Yapay Zeka ve Model Katmanı
Gemini 2.5 Flash (Google AI Studio): * Neden: Yüksek hız (low latency) ve güçlü görsel analiz (computer vision) yetenekleri.

Kullanım: Teknik grafiklerin (STEM) analizi, eksen tespiti ve akademik yorumlama süreçlerini yönetir.

Google Generative AI SDK: Python üzerinden Gemini modeline güvenli ve hızlı erişim sağlar.


3. Kullanıcı Arayüzü (Frontend & Backend)
Streamlit: Python ile hızlı ve reaktif web arayüzü geliştirme imkanı sunduğu için seçilmiştir.

Erişilebilirlik (A11y): Yüksek kontrastlı tema (CSS) ve ekran okuyucu uyumlu bileşenlerle desteklenmiştir.


4. Yardımcı Kütüphaneler ve Servisler
Edge-TTS (Microsoft Edge TTS): gTTS kütüphanesinden daha doğal ve insansı ses kalitesi sunduğu için tercih edilmiştir.

Streamlit Components (v1): JavaScript kodlarının Streamlit içerisine "enjekte" edilmesi ve tarayıcı olaylarının (kısayollar) dinlenmesi için kullanılmıştır.

Hashlib (MD5): Yüklenen görsellerin parmak izini alarak gereksiz API isteklerini önler ve sistem verimliliğini artırır.

Asyncio: Ses sentezleme işleminin kullanıcı arayüzünü kilitlemeden asenkron şekilde yürütülmesini sağlar.Ses sentezleme işleminin kullanıcı arayüzünü (UI) kilitlemeden arka planda yürütülmesi, özellikle görme engelli kullanıcıların ekran okuyucu akışının bozulmamasını sağlar.

5. Kurulum ve Gereksinimler
Projeyi yerel ortamda çalıştırmak için gerekli kütüphaneler aşağıdaki komut ile yüklenebilir:

pip install -r requirements.txt



