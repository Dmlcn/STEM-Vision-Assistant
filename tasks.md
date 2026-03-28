## STEM Vision Assistant (v1.1) - Görev Listesi (MVP)

Son güncelleme: 2026-03-25

### Hedef
Görme engelli üniversite öğrencilerinin teknik grafiklerin fotoğrafını yükleyip; grafik türü, eksen/birimler, trend ve kritik değişim noktalarını teknik terminolojiyle sesli olarak alabilmesini sağlayan “AI Laboratuvar Asistanı” MVP’sini tamamlamak.

### Başarı Kriterleri (KPIs)
- Teknik doğruluk: Grafik türü ve eğilim %85+.
- Erişilebilirlik: Ekran okuyucu kullanan kullanıcı için klavye/ses yardımıyla 1 dakika içinde tamamlanabilmeli.
- İşleme hızı: Fotoğraf yüklendikten sonra sesli yanıtın başlaması 12 saniyeyi geçmemeli.

### Notlar / Kapsam
- MVP kapsamına dahil: Teknik grafikler (P-V diyagramı, arz-talep eğrileri, devre şemaları vb.); sabit görsel analizi.
- MVP kapsamı dışında: Teknik olmayan görseller (matematiksel olmayan), el yazısı notların tam deşifresi, gerçek zamanlı video analizi.

---

## Milestone Bazlı Görevler (10 Gün)

### Gün 1: Proje iskeleti + temel arayüz
1. Python çalışma ortamını ve temel dosya yapısını oluştur.
   - Teslim: Streamlit uygulaması ayağa kalkıyor (`streamlit run ...`).
2. `requirements.txt` / bağımlılıkları belirle (Streamlit, Gemini client, TTS, görüntü işleme).
   - Teslim: `pip install -r requirements.txt` sorunsuz çalışıyor.
3. Basit UI iskeleti kur:
   - Dosya yükleme (kamera dahil “upload” akışı)
   - Grafik önizleme (erişilebilir şekilde)
   - Analiz başlatma butonu + durum mesajları
   - Teslim: Kullanıcı görsel seçip “Analiz et” diyebiliyor.

### Gün 2: Görsel doğrulama + ön işleme
4. Yüklenen görsel doğrulaması yap:
   - Dosya türü/uzunluk kontrolü, çok büyük dosyaları reddet
   - Teslim: Hatalar anlaşılır metin olarak ekrana yansıyor.
5. Ön işleme uygula:
   - Format standardizasyonu (RGB)
   - Gerekirse yeniden boyutlandırma/optimizasyon
   - Teslim: Model çağrısına uygun, tutarlı giriş görseli sağlanıyor.

### Gün 3: Akademik analiz motoru (Gemini Vision) entegrasyonu
6. Gemini Vision API entegrasyonunu ekle:
   - API anahtarı için env değişkenleri (`GEMINI_API_KEY`)
   - Zaman aşımı (timeout) ve hata yakalama
   - Teslim: Seçilen görsel Gemini’ye gönderiliyor ve ham yanıt alınıyor.
7. “STEM Uzmanı” prompt tasarımı:
   - Kullanıcı ihtiyacına göre çıktı şeması (örn. grafik türü, trend, eksenler/birimler, kritik noktalar)
   - Teknik terimlerle Türkçe anlatım
   - Teslim: Aynı tür grafiklerde tutarlı yapı döndüren bir prompt elde ediliyor.
8. Yanıtı yapılandır:
   - Model çıktısını parse ederek “temiz bir özet”e çevir
   - Teslim: Uygulama her seferinde konuşulabilir/okunabilir bir metin üretir.

### Gün 4: Kritik bilgi çıkarımı (tür + trend + kritik noktalar)
9. Çıktı formatını netleştir:
   - Grafik türü (lineer/log/parabolik vb.)
   - Eğilim (artan/azalan/üstel/kuvvet/eklips vb.)
   - Eksenler ve birimler
   - Zirve/dip/kırılma gibi kritik değişim noktaları
   - Teslim: Metin, kullanıcı için “akademik göz” ile anlaşılır hale gelir.
10. Hata senaryoları:
   - Model grafik türünü belirsiz bulursa nasıl davranılacak?
   - Eksen/birimler okunamıyorsa alternatif açıklama
   - Teslim: Çıktı bozulmuyor, kullanıcı yönlendirme alıyor.

### Gün 5: Sesli yanıt (TTS) entegrasyonu
11. TTS çözümünü ekle:
   - `gTTS` veya `pyttsx3` seçimi (projede karar ver)
   - Teslim: Model metnini ses dosyasına çevirip Streamlit’te çalabiliyoruz.
12. Ses başlatma akışı:
   - Analiz sırasında spinner/durum metni
   - Model yanıtı hazır olunca otomatik ses oynatma (uygun UX)
   - Teslim: “Sesli yanıtın başlaması” KPI hedefi için ölçülebilir şekilde çalışır.

### Gün 6: Erişilebilirlik ve kullanım akışı (1 dakika hedefi)
13. Klavye/erişilebilirlik iyileştirmeleri:
   - Buton/alanların etiketlenmesi
   - Hata mesajlarının ekran okuyucu dostu formatta olması
   - Metin alternatiflerinin sağlanması (ses + yazı birlikte)
   - Teslim: Ekran okuyucu ile akış testinde takılma yok.
14. Varsayılan ayarları optimize et:
   - Otomatik oynatma/manuel kontrol stratejisi
   - Gereksiz adımları kaldır
   - Teslim: Uygulama kullanım süresi 1 dakikanın içinde kalır.

### Gün 7: Performans ölçümü + hız optimizasyonu
15. Performans metriklerini logla:
   - Görsel upload -> model çağrısı başlama
   - Model yanıtı -> TTS üretimi
   - TTS üretimi -> sesin başlaması
   - Teslim: KPI’ya göre ölçüm mümkün.
16. Hız optimizasyonları:
   - Boyut/yeniden boyutlandırma ayarı
   - Önbellekleme (aynı görsel için)
   - Model/istem parametrelerini sadeleştirme
   - Teslim: Ses başlangıcı 12 saniye altında kalacak şekilde iyileştirilir.

### Gün 8: Kalite değerlendirme (Doğruluk %85 hedefi)
17. Test grafikleri oluştur / topla:
   - Mühendislik + Temel Bilim + İktisadi bilimden örnekler
   - Teslim: En az MVP doğrulaması için yeterli örnek seti var.
18. Değerlendirme süreci:
   - Grafik türü ve trend için basit skorlamalı değerlendirme
   - Teslim: %85 hedefi için eksiklerin kaydı tutulur.
19. Prompt/parse iyileştirmeleri:
   - Değerlendirme sonuçlarına göre prompt revizyonu
   - Parsing/format düzenlemeleri
   - Teslim: Doğruluk artar veya limitler belgelenir.

### Gün 9: Dayanıklılık + kullanıcı hatası yönetimi
20. Model/API hata dayanıklılığı:
   - Rate limit/timeout durumlarında geri dönüş
   - Kullanıcıya anlaşılır “tekrar dene” akışı
   - Teslim: Uygulama çökmeden yönetiyor.
21. Metin uzunluğu kontrolü:
   - Çok uzun çıktılarda TTS boğulmasını önle
   - Teslim: Ses çıktısı anlaşılır kalır.

### Gün 10: Dokümantasyon + teslim
22. `README.md` yaz:
   - Kurulum (API key dahil)
   - Kullanım
   - Erişilebilirlik / test notları
   - Teslim: Yeni bir geliştirici uygulamayı çalıştırabiliyor.
23. “MVP demo” senaryosu hazırla:
   - 3 farklı grafik tipi için adım adım akış
   - Teslim: Sunum/deneme için hazır.
24. Kapsam dışı maddeler için “gelecek plan” notu ekle:
   - Video analizi
   - El yazısı notlar
   - Teknik olmayan görseller
   - Teslim: Yol haritası net.

---

## Kabul / Çıkış Kontrol Listesi
- [ ] UI görsel alıp “Analiz et” akışı sunuyor.
- [ ] Analiz motoru Gemini Vision ile çalışıyor.
- [ ] Metin çıktısı teknik terminolojiyle tutarlı formatta.
- [ ] TTS ses oynatması yapılıyor.
- [ ] Ekran okuyucu ile kullanım akışı 1 dakikanın içinde denenebiliyor.
- [ ] Ses başlama KPI’sı için log/ölçüm var.
- [ ] Grafik türü + trend doğruluk değerlendirmesi yapılıyor (%85 hedefi).

