# KTÜN LMS Ders İçeriği İndirme Scripti

Bu script, Konya Teknik Üniversitesi (KTÜN) Öğrenme Yönetim Sistemi (LMS) üzerindeki ders içeriklerini otomatik olarak indirmek için geliştirilmiştir.

## Özellikler

- LMS'e otomatik giriş yapma
- Captcha'yı otomatik çözme (OpenCV ile)
- Ders içeriklerini Markdown formatında indirme
- Ders materyallerini (PDF, DOCX vb.) indirme (opsiyonel)

## Kurulum

1. Gerekli kütüphaneleri yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Chrome tarayıcısının yüklü olduğundan emin olun.

## Kullanım

```
python main.py -e <email> -p <şifre> -c <ders_id> [<ders_id> ...] [-d]
```

Parametreler:
- `-e`, `--email`: KTÜN uzantılı e-posta adresiniz (örn: f241202002@ktun.edu.tr)
- `-p`, `--password`: LMS şifreniz
- `-c`, `--course-ids`: İçeriği indirilecek derslerin ID'leri (boşluklarla ayırarak birden fazla girilebilir)
- `-d`, `--download`: Bu bayrak eklendiğinde, ders materyallerini (PDF, DOCX vb.) indirir

Örnek:
```
python main.py -e f241202002@ktun.edu.tr -p sifrem123 -c 15496 15848 -d
```

## Captcha Çözümü Hakkında

Bu script, LMS giriş sayfasındaki captcha'yı otomatik olarak çözmek için OpenCV kütüphanesini kullanır. Captcha, basit bir toplama işlemi içerir (örn: 5+3) ve görüntü işleme teknikleri kullanılarak çözülür.

### Avantajları

- Tesseract OCR'a göre daha hafif çözüm
- Ek motor kurulumu gerektirmez
- Kurulumu ve kullanımı daha kolay
- Sistem kaynaklarını daha az kullanır

### Çalışma Prensibi

1. Captcha resmi gri tonlamaya çevrilir
2. Gürültü azaltma ve adaptif eşikleme uygulanır
3. Konturlar bulunarak karakterler ayrıştırılır
4. Karakterler tanınır ve toplama işlemi gerçekleştirilir

## Sorun Giderme

Captcha çözümü başarısız olursa:
1. Captcha resminin net olduğundan emin olun
2. Manuel çözüm seçeneğini kullanın
3. OpenCV kütüphanesinin doğru şekilde yüklendiğinden emin olun

## Katkıda Bulunma

1. Bu repo'yu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.