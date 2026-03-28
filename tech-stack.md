Tech Stack: STEM Vision Assistant
Bu döküman, projenin geliştirilmesinde kullanılan teknolojileri ve bu teknolojilerin seçilme nedenlerini açıklar.

1. Programlama Dili
Python (v3.10+): Yapay zeka ve veri bilimi ekosistemindeki geniş kütüphane desteği ve öğrenme kolaylığı nedeniyle ana dil olarak seçilmiştir.


2. Yapay Zeka ve Model Katmanı
Gemini 1.5 Flash (Google AI Studio): * Neden: Yüksek hız (low latency) ve güçlü görsel analiz (computer vision) yetenekleri.

Kullanım: Teknik grafiklerin (STEM) analizi, eksen tespiti ve akademik yorumlama süreçlerini yönetir.

Google Generative AI SDK: Python üzerinden Gemini modeline güvenli ve hızlı erişim sağlar.


3. Kullanıcı Arayüzü (Frontend & Backend)
Streamlit: * Neden: Saf Python ile hızlı web arayüzü geliştirme imkanı sunması.

Erişilebilirlik: Standart bileşenlerinin ekran okuyucularla (Screen Readers) uyumlu çalışması ve 10 günlük geliştirme süreci için en verimli araç olması.


Gemini şunu dedi:
Harika bir ilerleme! tech-stack.md, projenin "mutfağında" hangi araçların olduğunu ve bu araçların neden seçildiğini anlatan teknik bir dökümandır. Bir mühendislik projesinde bu döküman, projenin sürdürülebilirliğini ve mantıksal çerçevesini gösterir.

İşte Notepad++ içine kopyalayıp tech-stack.md adıyla kaydedebileceğin profesyonel taslak:

🛠 Tech Stack: STEM Vision Assistant
Bu döküman, projenin geliştirilmesinde kullanılan teknolojileri ve bu teknolojilerin seçilme nedenlerini açıklar.

1. Programlama Dili
Python (v3.10+): Yapay zeka ve veri bilimi ekosistemindeki geniş kütüphane desteği ve öğrenme kolaylığı nedeniyle ana dil olarak seçilmiştir.

2. Yapay Zeka ve Model Katmanı
Gemini 1.5 Flash (Google AI Studio): * Neden: Yüksek hız (low latency) ve güçlü görsel analiz (computer vision) yetenekleri.

Kullanım: Teknik grafiklerin (STEM) analizi, eksen tespiti ve akademik yorumlama süreçlerini yönetir.

Google Generative AI SDK: Python üzerinden Gemini modeline güvenli ve hızlı erişim sağlar.

3. Kullanıcı Arayüzü (Frontend & Backend)
Streamlit: * Neden: Saf Python ile hızlı web arayüzü geliştirme imkanı sunması.

Erişilebilirlik: Standart bileşenlerinin ekran okuyucularla (Screen Readers) uyumlu çalışması ve 10 günlük geliştirme süreci için en verimli araç olması.

4. Yardımcı Kütüphaneler ve Servisler
gTTS (Google Text-to-Speech): AI tarafından üretilen akademik analizi, görme engelli kullanıcılar için anlık olarak sese dönüştürür.

Pillow (PIL): Kullanıcı tarafından yüklenen farklı formatlardaki (.jpg, .png) görsellerin işlenmesi ve AI modeline uygun hale getirilmesi için kullanılır.

Python-Dotenv: API anahtarlarının kod içerisinde açıkça görünmemesi ve güvenli bir şekilde yönetilmesi için tercih edilmiştir.


5. Kurulum ve Gereksinimler
Projeyi yerel ortamda çalıştırmak için gerekli kütüphaneler aşağıdaki komut ile yüklenebilir:

pip install streamlit google-generativeai gTTS Pillow python-dotenv




