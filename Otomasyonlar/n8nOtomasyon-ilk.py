#KTÜN YEMEKHANE REZERVASYON ALMA İLLETİNDEN KURTARMA SCRİPT'İ
import os
from PIL import Image
import pytesseract
from selenium.webdriver.chrome.options import Options
import html2text
import time

def otomasyonu_baslat(uniemail, unisifre):
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service as ChromeService
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support.ui import Select
    

    # tarayıcı - WebDriver'ı otomatik olarak indirir ve yönetir
    # Define download directory
    download_dir = os.path.join(os.getcwd(), "~/downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    chrome_options = Options()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    #bu uygulamada gerek yok ama kalsın nolcak
    def cookie_halledici(driver):
        try:
            cookie_accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "btn_cookie_ok"))
            )
            cookie_accept_button.click()
            print("🍪 Cookie pop-up'ı kabul edildi.")
            time.sleep(0.14)
        except Exception:
            print("ℹ️ Cookie pop-up'ı bulunamadı veya zaten kabul edilmiş.")
            pass

        # Giriş işlemleri
    driver.get("https://lms.ktun.edu.tr/login/login_auth.php")
    #cookie yok bu sitede 
    #cookie_halledici(driver    
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(uniemail)
    driver.find_element(By.ID, "bbbnh").send_keys(unisifre)
    driver.find_element(By.ID, "sozlesme").click()
    driver.find_element(By.ID, "sozlesme1").click()  
    # CAPTCHA resmini indir
    captcha_image = wait.until(EC.presence_of_element_located((By.ID, "captchaCanvas")))
    captcha_image.screenshot('captcha.png')
    print("🖼️ CAPTCHA resmi indirildi: captcha.png")
    # --- BAŞLANGIÇ: Otomatik CAPTCHA Çözümleme Kodu ---
    
    try:
            # CAPTCHA resmini yükle
            img = Image.open('captcha.png')

            # Resimden metin çıkar (OCR)
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            # Sadece rakamları tanıması için config: '--psm 6 outputbase digits'
            # Eğer '+' işareti de tanınmalıysa config='--psm 6' kullanılabilir.
            # Deneme yanılma ile en iyi config bulunabilir.
            captcha_text = pytesseract.image_to_string(img, config='--psm 6').strip()

            print(f"OCR ile okunan CAPTCHA metni: '{captcha_text}'")

            # Matematiksel işlemi yap
            calculated_captcha = ""
            if '+' in captcha_text:
                try:
                    parts = captcha_text.split('+')
                    num1 = int(''.join(filter(str.isdigit, parts[0]))) # Sadece rakamları al
                    num2 = int(''.join(filter(str.isdigit, parts[1]))) # Sadece rakamları al
                    calculated_captcha = str(num1 + num2)
                except ValueError:
                    print("OCR ile okunan metin sayısal işleme uygun değil.")
                    calculated_captcha = "" # Hata durumunda boş bırak
            else:
                # Eğer OCR sadece sonucu okursa veya farklı bir format gelirse
                calculated_captcha = ''.join(filter(str.isdigit, captcha_text)) # Sadece rakamları al

            if not calculated_captcha:
                raise ValueError("CAPTCHA metni işlenemedi veya boş.")

            print(f"Hesaplanan CAPTCHA sonucu: '{calculated_captcha}'")
            captcha_code = calculated_captcha # Otomatik çözülen kodu ata

    except Exception as e:
                   print(f"❌ Otomatik CAPTCHA çözümlemesinde hata oluştu: {e}")
                   print("Otomatik çözüm başarısız, manuel CAPTCHA girişi bekleniyor...")
                   # Hata durumunda manuel girişe geri dönmek için captcha_code'u None yap
                   captcha_code = None
        # --- SON: Otomatik CAPTCHA Çözümleme Kodu ---

    driver.find_element(By.ID, "captchaInput").send_keys(calculated_captcha)
    driver.find_element(By.ID, "loginbtn").click()
 
  # Girişin başarılı olup olmadığını kontrol etmek için bekle
  # try:
  #     WebDriverWait(driver, 15).until(
  #         EC.presence_of_element_located((By.ID, "yui_3_17_2_1_1755116919169_52"))
  #     )
  #     print("✅ Giriş başarılı!")
  # except Exception as e:
  #     print("❌ Giriş başarısız oldu veya çok uzun sürdü. Sayfa içeriğini kontrol edin")
  #     driver.quit()
  #     return # Fonksiyondan çık
    time.sleep(2)   # Sayfanın tamamen yüklenmesini bekle
    # Navigate to a specific course page after successful login
    inkilapTarih = 15848
    BilgDestkTeknik = 15849
    BİlgProg = 15853
    FizikII = 15496
    course_id = 15496
    
    course_url = f"https://lms.ktun.edu.tr/course/view.php?id={course_id}"
    print(f"Kurs sayfasına gidiliyor: {course_url}")
    driver.get(course_url)

    # Sayfanın tamamen yüklenmesini bekle
    time.sleep(2)
    # Sayfa kaynağını (HTML) al
    html_content = driver.page_source

    # HTML'i Markdown'a çevir
    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown_content = h.handle(html_content)

    # Markdown içeriğini dosyaya yaz
    md_filename = f"course_{course_id}.md"
    try:
        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        print(f"📄 Kurs içeriği başarıyla '{md_filename}' dosyasına kaydedildi.")
    except Exception as e:
        print(f"❌ Markdown dosyası yazılırken bir hata oluştu: {e}")

    # İşlem bitti, tarayıcıyı kapat
    print("İşlem tamamlandı. Tarayıcı kapatılıyor.")
    driver.quit()

otomasyonu_baslat("f241202002@ktun.edu.tr", "980511Bnff42.uni")