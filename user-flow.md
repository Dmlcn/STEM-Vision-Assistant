Kullanıcı Akışı (User Flow): STEM Vision Assistant


Bu döküman, bir görme engelli öğrencinin uygulamayı açtığı andan analizi dinlediği ana kadar geçen süreci adım adım tanımlar.

Adım,Kullanıcı Eylemi,Sistem Yanıtı / Geri Bildirim
1. Giriş,Uygulama URL'sini açar.,"Ekran okuyucu başlığı okur: ""STEM Vision Assistant. Lütfen bir grafik yükleyin."""
2. Yükleme,"""Dosya Seç"" butonuna tıklar.",İşletim sistemi dosya seçicisi açılır. Kullanıcı görseli seçer.
3. Onay,Görseli yükler.,"Sistem sesli uyarı verir: ""Görsel başarıyla yüklendi. Analizi başlatmak için tıklayın."""
4. İşleme,"""Analizi Başlat"" butonuna tıklar.","""Analiz ediliyor..."" uyarısı çıkar (Spinner). AI görseli işler."
5. Sonuç,Analizin bitmesini bekler.,Akademik analiz metni ekranda belirir ve odak bu metne kayar.
6. Seslendirme,(Otomatik),"Sistem, üretilen analizi otomatik olarak sesli okumaya başlar (Auto-play TTS)."
7. Tekrar,"""Tekrar Dinle"" butonuna tıklar.",Mevcut analiz metni tekrar seslendirilir.


2. Erişilebilirlik Detayları (A11y)
Uygulama tasarlanırken şu erişilebilirlik standartları baz alınmıştır:

Semantik HTML: Tüm butonlar ve giriş alanları ekran okuyucuların (TalkBack/VoiceOver) anlayabileceği standart etiketlerle (<button>, <input>) oluşturulacaktır.

Odak Yönetimi: Analiz tamamlandığında, ekran okuyucunun odağı otomatik olarak sonuç metnine kaydırılarak kullanıcının sayfada kaybolması engellenecektir.

Sesli Geri Bildirim: Sadece sonuç değil, yükleme ve işlem süreçleri de kısa sesli bildirimlerle (Örn: "Yükleme tamamlandı") desteklenecektir.

Yüksek Kontrast: Arayüz, az gören kullanıcılar için yüksek kontrastlı (Siyah arka plan üzerine beyaz/sarı metin) bir tema ile sunulacaktır.


3. Hata Senaryoları
Hatalı Dosya: Kullanıcı grafik olmayan bir görsel yüklerse; AI bunu tespit eder ve "Hata: Bu bir teknik grafik değil. Lütfen bir STEM görseli yükleyin." uyarısı verir.

Bağlantı Sorunu: API bağlantısı koparsa; "Sunucuya ulaşılamıyor, lütfen internet bağlantınızı kontrol edin." uyarısı sesli olarak okunur.