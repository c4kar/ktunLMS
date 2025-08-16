import argparse
from n8nOtomasyon import otomasyonu_baslat

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="KTÜN LMS sisteminden ders içeriklerini indiren otomasyon script'i.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "-e", "--email", 
        required=True, 
        help="KTÜN e-posta adresiniz (örn: f241202002@ktun.edu.tr)"
    )
    parser.add_argument(
        "-p", "--password", 
        required=True, 
        help="LMS şifreniz."
    )
    parser.add_argument(
        "-c", "--course-ids", 
        required=True, 
        nargs='+', 
        help="İçeriği indirilecek derslerin ID'leri (*boşluklarla ayırarak birden fazla girilebilir)."
    )
    parser.add_argument(
        "-d", "--download",
        action="store_true",
        required=False,
        help="Bu bayrak eklendiğinde, ders materyallerini (PDF, DOCX vb.) indirir.\nÖrnek kullanım:\npy main.py -e <email> -p <şifre> -c 15496 15848 -d"
    )
    
    args = parser.parse_args()
    # args.download
    # Ana fonksiyonu diğer dosyadan çağır.
    otomasyonu_baslat(args.email, args.password, args.course_ids, args.download)