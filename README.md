# Sigorta Acentesi Sosyal Medya Asistanı 🛡️

Bu uygulama, sigorta acenteleri için yapay zeka destekli (ChatGPT & DALL-E) Instagram içerikleri üretir. Günlük konu fikirleri bulur, metin yazar ve görsel oluşturur.

## Kurulum

1.  Bilgisayarınızda Python'un kurulu olduğundan emin olun.
2.  Bu klasörde bir terminal/komut satırı açın.
3.  Gerekli kütüphaneleri yükleyin:
    ```bash
    pip install -r requirements.txt
    ```

## Ayarlar (API Anahtarı)

1.  Bu klasördeki `.env.example` dosyasının adını `.env` olarak değiştirin.
2.  `.env` dosyasını not defteri ile açın.
3.  `OPENAI_API_KEY=sk-...` kısmına kendi OpenAI API anahtarınızı yapıştırın.

## Çalıştırma

Uygulamayı başlatmak için terminale şu komutu yazın:

```bash
streamlit run app.py
```

Tarayıcınız otomatik olarak açılacak ve uygulamayı kullanmaya başlayabileceksiniz.

## Kullanım

1.  **"Yeni Konu Fikirleri Bul"** butonuna tıklayın.
2.  Size sunulan 3 fikirden birini seçin.
3.  **"Metin ve Görsel Oluştur"** butonuna tıklayın (Biraz zaman alabilir).
4.  Oluşturulan içeriği inceleyin.
5.  **"Dosyaları Kaydet"** butonuna tıklayarak bilgisayarınıza (`olusturulan_icerikler` klasörüne) kaydedin.
6.  Kaydedilen dosyaları Instagram'a manuel olarak yükleyin.
