from bs4 import BeautifulSoup

# HTML dosyasını oku
with open('Kurslarım _ KTUN _ LMS.htm', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup ile HTML'i parse et
soup = BeautifulSoup(html_content, 'html.parser')

# Kurs divlerini bul
course_divs = soup.find_all('div', class_='course-listitem')

# İki dosyayı da yazma modunda aç
with open('eemDersID.md', 'w', encoding='utf-8') as md_file, \
     open('id_and_titles.txt', 'w', encoding='utf-8') as txt_file:

    for course_div in course_divs:
        course_id = course_div.get('data-course-id')
        course_name_tag = course_div.find('a', class_='coursename')

        if course_id and course_name_tag:
            course_name = course_name_tag.get_text(separator=' ', strip=True).replace('Kurs Adı', '').strip()

            # Markdown dosyasına yaz
            md_file.write(f'''{course_id} - [# {course_name}](https://lms.ktun.edu.tr/course/view.php?id={course_id})

''')

            # TXT dosyasına yaz
            txt_file.write(f"ID: {course_id}, Title: {course_name}\n")

print(f'{len(course_divs)} adet kurs işlendi ve ilgili dosyalara yazıldı.')
