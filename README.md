## Problem
Bilim, Teknoloji, Mühendislik ve Matematik (STEM) eğitiminde kullanılan görsel materyaller (grafikler, fonksiyonlar, mühendislik diyagramları), görme engelli öğrenciler için erişilebilirlik bariyeri oluşturmaktadır. Bu öğrencilerin karmaşık görsel verileri bağımsız bir şekilde anlamlandırması ve takip etmesi oldukça zordur.

## Çözüm
STEM Vision Assistant, bu bariyeri ortadan kaldırmak için tasarlanmış yapay zeka tabanlı bir erişilebilirlik aracıdır. En güncel Gemini 2.5 Flash modelini kullanarak görselleri saniyeler içinde analiz eder. Sadece görseli betimlemekle kalmaz; dinleyicinin zihninde bir koordinat sistemi kurabilmesi için mekansal rehberlik sağlar. Analiz sonuçları, Edge-TTS altyapısıyla doğal bir insan sesiyle seslendirilerek kullanıcıya sunulur.

## Canlı Demo
Yayın Linki: https://stemvisionassistant.streamlit.app

Demo Video: https://www.loom.com/share/de0211741381429da783b4b6403cf7ee

## Kullanılan Teknolojiler
Python: Ana programlama dili.

Streamlit: Modern ve hızlı web arayüzü.

Google Gemini 2.5 Flash API: Görsel analiz ve akıllı betimleme motoru.

Microsoft Edge-TTS: Yüksek kaliteli, doğal metin-konuşma (TTS) motoru.

Modüler Mimari: Sürdürülebilir kod yapısı için features/ klasörü altında paketlenmiş mantıksal katmanlar.

## Nasıl Çalıştırılır?
Uygulamayı yerel bilgisayarınızda çalıştırmak için şu adımları izleyebilirsiniz:

1-) Gereksinimleri Yükleyin:

pip install -r requirements.txt

2- )API Anahtarını Ayarlayın:

.env dosyası oluşturun ve GEMINI_API_KEY değişkenini ekleyin.

3-)Uygulamayı Başlatın 

python -m streamlit run features/app.py
