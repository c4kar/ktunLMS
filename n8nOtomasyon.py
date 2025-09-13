# KTÜN LMS DERS İÇERİĞİ İNDİRME SCRİPTİ
import os
import argparse
import time
import re
import requests
from PIL import Image
# Tesseract OCR yerine OpenCV kullanılıyor
import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def extract_course_content(driver, course_id):
    """
    Verilen bir ders ID'si için ders sayfasını ziyaret eder,
    içeriği ayrıştırır ve yapılandırılmış bir Markdown metni olarak döndürür.
    """
    course_url = f"https://lms.ktun.edu.tr/course/view.php?id={course_id}"
    print(f"\n▶️  Kurs sayfasına gidiliyor: {course_url}")
    driver.get(course_url)
    
    try:
        # Sayfanın yüklenmesini bekle (örneğin, kurs başlığı görünene kadar)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        time.sleep(1) # Dinamik içeriklerin yüklenmesi için ek bekleme
    except Exception as e:
        print(f"❌ Kurs sayfası yüklenemedi veya başlık bulunamadı: {e}")
        return None, None

    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    course_title = soup.find('h1').get_text(strip=True) if soup.find('h1') else f"Ders-{course_id}"
    # Dosya adları için geçersiz karakterleri temizle
    safe_course_title = "".join(c for c in course_title if c.isalnum() or c in (' ', '-')).rstrip()

    print(f"📄 '{course_title}' dersi için içerik ayrıştırılıyor...")

    markdown_content = f"# {course_title}\n\n"
    
    # Moodle'un haftalık/konulu yapısını bul (genellikle 'ul.topics' veya benzeri)
    sections = soup.find_all('li', class_='section')

    if not sections:
        markdown_content += "Bu derste herhangi bir konu bölümü bulunamadı.\n"
        return safe_course_title, markdown_content

    for section in sections:
        section_title_elem = section.find(['h3', 'h4'], class_='sectionname')
        if not section_title_elem:
            continue
            
        section_title = section_title_elem.get_text(strip=True)
        markdown_content += f"## {section_title}\n\n"

        # Bölüm özetini/notlarını bul (data-for="sectioninfo")
        section_info_elem = section.find('div', attrs={'data-for': 'sectioninfo'})
        if section_info_elem:
            section_info_text = section_info_elem.get_text(separator='\n', strip=True)
            if section_info_text:
                # Çok satırlı blockquote'ları doğru formatlamak için her satırın başına '> ' ekle
                formatted_info = '\n'.join(f'> {line}' for line in section_info_text.splitlines() if line.strip())
                if formatted_info:
                    markdown_content += f"{formatted_info}\n\n"

        # Bölüm içindeki aktivite ve kaynakları bul
        activities = section.find_all('li', class_=['activity', 'resource'])
        if not activities:
            markdown_content += "- Bu bölümde içerik bulunmuyor.\n"
        else:
            for activity in activities:
                instance_name_elem = activity.find('span', class_='instancename')
                activity_link_elem = activity.find('a')
                
                if instance_name_elem and activity_link_elem:
                    instance_name = instance_name_elem.get_text(strip=True)
                    activity_link = activity_link_elem['href']
                    activity_type = instance_name_elem.find_next_sibling('span').get_text(strip=True) if instance_name_elem.find_next_sibling('span') else ""
                    
                    # Ana aktivite satırını ekle
                    markdown_content += f"- **{instance_name}** ({activity_type}): [Link]({activity_link})\n"
                    
                    # Aktiviteye ait açıklamayı (notu) bul
                    description_elem = activity.find('div', class_='description')
                    if description_elem:
                        description_text = description_elem.get_text(separator='\n', strip=True)
                        if description_text:
                            # Açıklamayı girintili bir blockquote olarak formatla
                            formatted_description = '\n'.join(f'  > {line}' for line in description_text.splitlines() if line.strip())
                            if formatted_description:
                                markdown_content += f"{formatted_description}\n"
        
        markdown_content += "\n"

    return safe_course_title, markdown_content

# Şablon eşleştirme ile captcha çözüm fonksiyonu
def solve_captcha_with_templates(captcha_path, templates_dir='templates'):
    """
    Şablon eşleştirme kullanarak captcha'yı çözer.
    
    Args:
        captcha_path: Captcha resminin dosya yolu
        templates_dir: Şablon görüntülerinin bulunduğu klasör
        
    Returns:
        str: Hesaplanan captcha sonucu veya None (başarısız olursa)
    """
    try:
        # Şablon görüntülerini yükle
        templates = {}
        for i in range(10):
            template_path = os.path.join(templates_dir, f"{i}.png")
            if os.path.exists(template_path):
                templates[str(i)] = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
        
        plus_path = os.path.join(templates_dir, "plus.png")
        if os.path.exists(plus_path):
            templates["+"] = cv2.imread(plus_path, cv2.IMREAD_GRAYSCALE)
        
        # Şablon görüntüleri bulunamazsa, mevcut yönteme geri dön
        if not templates:
            print("⚠️ Şablon görüntüleri bulunamadı, piksel yoğunluğu analizi kullanılıyor...")
            return solve_captcha_with_opencv(captcha_path)
        
        # Captcha resmini oku ve gri tonlamaya çevir
        img = cv2.imread(captcha_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Gürültü azaltma
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptif eşikleme
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morfolojik işlemler
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Konturları bul
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Konturları soldan sağa sırala
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
        
        # Her bir kontur için karakter tanıma
        characters = []
        for contour in contours:
            # Konturun sınırlayıcı dikdörtgenini al
            x, y, w, h = cv2.boundingRect(contour)
            
            # Çok küçük konturları atla (gürültü olabilir)
            if w < 10 or h < 10:
                continue
                
            # Karakteri kırp
            char_roi = thresh[y:y+h, x:x+w]
            
            # Karakteri yeniden boyutlandır (normalizasyon)
            # Şablonlarla aynı boyuta getir
            template_height, template_width = next(iter(templates.values())).shape[:2]
            resized_char = cv2.resize(char_roi, (template_width, template_height))
            
            # Şablon eşleştirme
            best_match = None
            best_score = float('inf')
            
            for char, template in templates.items():
                # Şablon ile karakter arasındaki farkı hesapla
                # Normalize edilmiş kare fark yöntemi kullanılıyor
                result = cv2.matchTemplate(resized_char, template, cv2.TM_SQDIFF_NORMED)
                min_val, _, min_loc, _ = cv2.minMaxLoc(result)
                
                # En düşük fark değeri en iyi eşleşmeyi gösterir
                if min_val < best_score:
                    best_score = min_val
                    best_match = char
            
            # Eşleşme skoru belirli bir eşik değerinden düşükse kabul et
            if best_score < 0.5:  # Eşik değeri ayarlanabilir
                characters.append(best_match)
            else:
                print(f"⚠️ Karakter tanınamadı, eşleşme skoru: {best_score}")
        
        # Karakterleri birleştir
        captcha_text = ''.join(characters)
        print(f"Şablon eşleştirme ile okunan CAPTCHA metni: '{captcha_text}'")
        
        # Toplama işlemini gerçekleştir
        parts = captcha_text.split('+')
        if len(parts) == 2:
            try:
                num1 = int(parts[0])
                num2 = int(parts[1])
                calculated_captcha = str(num1 + num2)
                print(f"✅ Hesaplanan CAPTCHA sonucu: '{calculated_captcha}'")
                return calculated_captcha
            except ValueError:
                raise Exception("Sayılar doğru tanımlanamadı")
        else:
            raise Exception("CAPTCHA metni doğru formatta değil")
            
    except Exception as e:
        print(f"❌ Şablon eşleştirme ile CAPTCHA çözümlemesi başarısız: {e}")
        print("⚠️ Piksel yoğunluğu analizi yöntemine geri dönülüyor...")
        return solve_captcha_with_opencv(captcha_path)

# OpenCV ile captcha çözüm fonksiyonu (piksel yoğunluğu analizi)
def solve_captcha_with_opencv(captcha_path):
    """
    OpenCV kullanarak captcha'yı çözer.
    Basit toplama işlemi içeren captcha'lar için optimize edilmiştir.
    
    Args:
        captcha_path: Captcha resminin dosya yolu
        
    Returns:
        str: Hesaplanan captcha sonucu veya None (başarısız olursa)
    """
    try:
        # Resmi oku ve gri tonlamaya çevir
        img = cv2.imread(captcha_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Gürültü azaltma
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Adaptif eşikleme
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, 11, 2)
        
        # Morfolojik işlemler
        kernel = np.ones((3, 3), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Konturları bul
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Konturları soldan sağa sırala
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
        
        # Her bir kontur için karakter tanıma
        characters = []
        for contour in contours:
            # Konturun sınırlayıcı dikdörtgenini al
            x, y, w, h = cv2.boundingRect(contour)
            
            # Çok küçük konturları atla (gürültü olabilir)
            if w < 10 or h < 10:
                continue
                
            # Karakteri kırp
            char_roi = thresh[y:y+h, x:x+w]
            
            # Karakteri tanı
            aspect_ratio = w / h
            
            if 0.8 < aspect_ratio < 1.2 and w < 30:  # Kare şekli, muhtemelen "+"
                characters.append("+")
            else:  # Sayı
                # Karakteri yeniden boyutlandır (normalizasyon)
                resized_char = cv2.resize(char_roi, (20, 30))
                
                # Piksel yoğunluğunu hesapla
                pixel_density = cv2.countNonZero(resized_char) / (20 * 30)
                
                # Piksel yoğunluğuna göre sayıyı tahmin et
                # Bu değerler test edilip optimize edilmelidir
                if pixel_density < 0.3:
                    characters.append("1")
                elif pixel_density < 0.4:
                    characters.append("7")
                elif pixel_density < 0.5:
                    characters.append("4")
                elif pixel_density < 0.6:
                    characters.append("2")
                elif pixel_density < 0.7:
                    characters.append("3")
                elif pixel_density < 0.8:
                    characters.append("5")
                elif pixel_density < 0.9:
                    characters.append("6")
                else:
                    characters.append("8")
        
        # Karakterleri birleştir
        captcha_text = ''.join(characters)
        print(f"OpenCV ile okunan CAPTCHA metni: '{captcha_text}'")
        
        # Toplama işlemini gerçekleştir
        parts = captcha_text.split('+')
        if len(parts) == 2:
            try:
                num1 = int(parts[0])
                num2 = int(parts[1])
                calculated_captcha = str(num1 + num2)
                print(f"✅ Hesaplanan CAPTCHA sonucu: '{calculated_captcha}'")
                return calculated_captcha
            except ValueError:
                raise Exception("Sayılar doğru tanımlanamadı")
        else:
            raise Exception("CAPTCHA metni doğru formatta değil")
            
    except Exception as e:
        print(f"❌ OpenCV ile CAPTCHA çözümlemesi başarısız: {e}")
        return None

def otomasyonu_baslat(uniemail, unisifre, course_ids, download_documents=False):
    """
    Ana otomasyon fonksiyonu. LMS'e giriş yapar ve verilen ders ID'leri için içerik çeker.
    
    Args:
        uniemail: KTÜN uzantılı e-posta adresi
        unisifre: LMS şifresi
        course_ids: İçeriği indirilecek derslerin ID'leri
        download_documents: True ise, ders materyallerini (PDF, DOCX vb.) indirir
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Arayüzü gizlemek için
    chrome_options.add_argument("--log-level=3") # Konsol loglarını temizler
    
    # Temel indirme ayarlarını yapılandır
    # Not: Ders-spesifik indirme dizini daha sonra her ders için ayrı ayrı ayarlanacak
    prefs = {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False,
        "plugins.always_open_pdf_externally": True  # PDF'leri tarayıcıda açmak yerine indir
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)
    
    print("ℹ️ LMS giriş sayfasına gidiliyor...")
    driver.get("https://lms.ktun.edu.tr/login/login_auth.php")
    
    wait.until(EC.presence_of_element_located((By.ID, "username"))).send_keys(uniemail)
    driver.find_element(By.ID, "bbbnh").send_keys(unisifre)
    driver.find_element(By.ID, "sozlesme").click()
    driver.find_element(By.ID, "sozlesme1").click()  
    
    captcha_image = wait.until(EC.presence_of_element_located((By.ID, "captchaCanvas")))
    captcha_image.screenshot('captcha.png')
    print("🖼️ CAPTCHA resmi indirildi: captcha.png")
    
    try:
        # Şablon eşleştirme ile captcha çözümü
        calculated_captcha = solve_captcha_with_templates('captcha.png')
        if not calculated_captcha:
            print("⚠️ Otomatik çözüm başarısız oldu, manuel giriş isteniyor...")
            calculated_captcha = input("Lütfen resimdeki CAPTCHA sonucunu manuel girin: ")
    except Exception as e:
        print(f"❌ Otomatik CAPTCHA çözümlemesi başarısız: {e}")
        calculated_captcha = input("Lütfen resimdeki CAPTCHA sonucunu manuel girin: ")

    driver.find_element(By.ID, "captchaInput").send_keys(calculated_captcha)
    driver.find_element(By.ID, "loginbtn").click() 
 
    try:
        # Girişin başarılı olduğunu doğrulamak için kullanıcı adının göründüğü bir elementi bekle
        user_profile_name = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".userinitials"))
        ).text
        print(f"\n✅ Giriş başarılı! Hoş geldin, {user_profile_name}.")
    except Exception:
        print("\n❌ Giriş başarısız oldu. Lütfen e-posta, şifre ve CAPTCHA bilgilerini kontrol edin.")
        driver.quit()
        return

    # Ders içeriklerini çekme
    for course_id in course_ids:
        course_title, markdown_content = extract_course_content(driver, course_id)
        
        if course_title and markdown_content:
            md_filename = f"{course_title}.md"
            try:
                with open(md_filename, "w", encoding="utf-8") as f:
                    f.write(markdown_content)
                print(f"✅ Kurs içeriği başarıyla '{md_filename}' dosyasına kaydedildi.")
            except Exception as e:
                print(f"❌ Markdown dosyası yazılırken bir hata oluştu: {e}")

            # MD dosyasındaki linkleri tarayıp belgeleri indir (opsiyonel)
            if course_title and download_documents:
                print(f"\n📥 Belge indirme seçeneği aktif. '{md_filename}' dosyasındaki belgeler indiriliyor...")
                
                # Her ders için ayrı bir indirme klasörü oluştur
                download_dir = os.path.abspath(f"LMS_Downloads/{course_title}")
                os.makedirs(download_dir, exist_ok=True)
                print(f"📁 Dosyalar şu klasöre indirilecek: {download_dir}")
                
                # Chrome'un indirme dizinini bu ders için güncelle
                driver.execute_cdp_cmd('Page.setDownloadBehavior', {
                    'behavior': 'allow',
                    'downloadPath': download_dir
                })
                
                # Belgeleri indir
                download_documents_from_md(driver, md_filename, course_title)
            elif course_title:
                print(f"\nℹ️ Belge indirme seçeneği aktif değil. Belgeleri indirmek için -d parametresini kullanın.")
                
    print("\n🎉 Tüm işlemler tamamlandı. Tarayıcı kapatılıyor.")
    driver.quit()

def download_documents_from_md(driver, md_filename, course_title):
    """
    MD dosyasındaki linkleri tarayıp belgeleri doğrudan indirir.
    """
    print(f"\n📄 '{md_filename}' dosyasındaki linkler taranıyor...")
    
    try:
        with open(md_filename, "r", encoding="utf-8") as f:
            md_content = f.read()
    except Exception as e:
        print(f"❌ MD dosyası okunurken bir hata oluştu: {e}")
        return
    
    # Markdown link formatını bul: [Link Metni](URL)
    link_pattern = r'\[.*?\]\((https?://[^\s\)]+)\)'
    links = re.findall(link_pattern, md_content)
    
    if not links:
        print("⚠️ MD dosyasında hiç link bulunamadı.")
        return
    
    print(f"🔍 Toplam {len(links)} link bulundu.")
    
    # Belgeleri indirmek için klasör yolunu al (klasör zaten oluşturuldu)
    download_dir = os.path.abspath(f"LMS_Downloads/{course_title}")
    
    for i, link in enumerate(links, 1):
        print(f"\n🔗 Link {i}/{len(links)}: {link}")
        
        try:
            # Linke git (tarayıcı oturumunu kullanmak için)
            driver.get(link)
            time.sleep(2)  # Sayfanın yüklenmesi için bekle
            
            # Dosya indirme işlemi
            try:
                # Mevcut URL'yi al (yönlendirmelerden sonra)
                current_url = driver.current_url
                
                # Tarayıcı oturumunun çerezlerini kullanarak dosyayı indir
                headers = {
                    'User-Agent': driver.execute_script("return navigator.userAgent"),
                    'Referer': driver.current_url
                }
                response = requests.get(
                    current_url,
                    cookies={c['name']: c['value'] for c in driver.get_cookies()},
                    headers=headers,
                    stream=True,
                    allow_redirects=True
                )
                
                # Dosya adını belirle
                if "Content-Disposition" in response.headers:
                    # Content-Disposition header'ından dosya adını çıkar
                    content_disp = response.headers["Content-Disposition"]
                    filename_match = re.search(r'filename="(.+?)"', content_disp)
                    if filename_match:
                        filename = filename_match.group(1)
                    else:
                        filename = f"dosya_{i}"
                else:
                    # URL'den dosya adını çıkar
                    filename = current_url.split("/")[-1].split("?")[0]
                    if not filename or len(filename) < 3:
                        # Sayfa başlığını kullan
                        filename = "".join(c for c in driver.title if c.isalnum() or c in (' ', '-', '_', '.')).rstrip()
                        # Uzantı ekle
                        if not any(filename.lower().endswith(ext) for ext in ['.pdf', '.pptx', '.ppt', '.docx', '.doc', '.xlsx', '.xls', '.rar', '.zip','.php']):
                            # İçerik türüne göre uzantı belirle
                            content_type = response.headers.get('Content-Type', '')
                            if 'pdf' in content_type:
                                filename += '.pdf'
                            elif 'powerpoint' in content_type or 'presentation' in content_type:
                                filename += '.pptx'
                            elif 'word' in content_type or 'document' in content_type:
                                filename += '.docx'
                            elif 'excel' in content_type or 'spreadsheet' in content_type:
                                filename += '.xlsx'
                            elif 'zip' in content_type or 'compressed' in content_type:
                                filename += '.zip'
                            elif 'html' in content_type:
                                filename += '.html'
                            else:
                                filename += '.bin'  # Bilinmeyen dosya türü
                
                # Dosya yolu oluştur
                file_path = os.path.join(download_dir, filename)
                
                # Dosyayı kaydet
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                print(f"✅ Dosya başarıyla indirildi: {file_path}")
                
            except Exception as e:
                print(f"❌ Dosya indirilirken bir hata oluştu: {e}")
                
                # Hata durumunda sayfayı HTML olarak kaydet
                try:
                    page_title = driver.title
                    safe_page_title = "".join(c for c in page_title if c.isalnum() or c in (' ', '-')).rstrip()
                    
                    # Sayfalar klasörü oluştur
                    pages_dir = f"{download_dir}/Sayfalar"
                    os.makedirs(pages_dir, exist_ok=True)
                    
                    html_filename = f"{pages_dir}/{safe_page_title}.html"
                    with open(html_filename, "w", encoding="utf-8") as f:
                        f.write(driver.page_source)
                    print(f"✅ Sayfa HTML olarak kaydedildi: {html_filename}")
                except Exception as html_error:
                    print(f"❌ Sayfa HTML olarak kaydedilemedi: {html_error}")
            
        except Exception as e:
            print(f"❌ Linke gidilirken bir hata oluştu: {e}")
    
    print(f"\n✅ '{md_filename}' dosyasındaki tüm linkler tarandı ve belgeler indirildi.")

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="KTÜN LMS sisteminden ders içeriklerini indiren otomasyon script'i.",
#         formatter_class=argparse.RawTextHelpFormatter
#     )
#     parser.add_argument(
#         "-e", "--email", 
#         required=True, 
#         help="KTÜN uzantılı e-posta adresiniz (örn: f241202002@ktun.edu.tr)"
#     )
#     parser.add_argument(
#         "-p", "--password", 
#         required=True, 
#         help="LMS şifreniz."
#     )
#     parser.add_argument(
#     "-c", "--course-ids",
#         required=True, 
#         nargs='+', 
#         help="İçeriği indirilecek derslerin ID'leri (boşluklarla ayırarak birden fazla girilebilir).\n Örnek kullanım:\n"
#     ) 