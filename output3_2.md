# Bilgisayar Programlama 1 {#bilgisayar-programlama-1}

## Ders Notu 8 - Sıralama ve Arama {#ders-notu-8-siralamave-arama}

### Genel Bakış

Bu ders notu, diziler ve matrisler üzerinde gerçekleştirilen temel işlemlerden olan arama ve sıralama algoritmalarını ele almaktadır. Veri yapıları üzerinde hızlı ve etkili çözümler üretmek için doğru algoritma seçimi ve uygulanması büyük önem taşır. Not, özellikle doğrusal arama, ikili arama, kabarcık sıralama ve hızlı sıralama algoritmalarını örnek kodlar ve açıklamalarla detaylandırmaktadır. Ayrıca, bu bilgileri pekiştirmek amacıyla ödev soruları da sunulmuştur.

### İçindekiler {# 1}

1.  [Giriş](#giriş)
2.  [Dizilerde Arama ve Sıralama](#dizilerdea&s)
3.  [Dizilerde Arama](#dizilerdearama)
    *   [Doğrusal Arama (Linear / Sequential Search)](#doğrusalarama)
    *   [İkili Arama (Binary Search)](#ikiliarama)
4.  [Dizilerde Sıralama](#dizilerdesıralama)
    *   [Kabarcık Sıralama (Bubble Sort)](#kabarcıksıralama)
    *   [Hızlı Sıralama (Quick Sort)](#hızlısıralama)
5.  [Ödev Soruları](#ödevsoruları)
    *   [Ödev 1](#ödev-1)
    *   [Ödev 2](#ödev-2)
6.  [Kaynaklar](#kaynaklar)

## Giriş {#giriş}

Diziler ve matrisler, programlamada belirli veri kümelerini gruplandırmak ve yönetmek için temel araçlardır. Bu veri yapıları, özellikle sıralama ve arama gibi operasyonları gerçekleştirirken büyük kolaylık sağlar. Farklı değişkenlere dağılmış veriler yerine dizilerde tutulan verilerle çalışmak, karmaşıklığı önemli ölçüde azaltır.

## Dizilerde Arama ve Sıralama {#dizilerdea&s}

Arama ve sıralama algoritmaları, yazılım geliştirme dünyasında hem akademik hem de endüstriyel açıdan kritik bir öneme sahiptir. Özellikle büyük veri kümeleriyle çalışırken, aranan verilere en hızlı şekilde erişmek doğru algoritma seçimine bağlıdır. Bu nedenle, bu algoritmaların etkin bir şekilde anlaşılması ve uygulanması, verimlilik açısından büyük fark yaratır.

## Dizilerde Arama {#dizilerdearama}

Dizilerde arama, belirli bir elemanın dizide bulunup bulunmadığını tespit etme işlemidir. Bu süreçte, dizinin belirli bir arama değerine sahip bir eleman içerip içermediği kontrol edilir. İki temel arama tekniği incelenecektir: Doğrusal Arama ve İkili Arama.

### Doğrusal Arama (Linear / Sequential Search) {#doğrusalarama}

Doğrusal arama, sıralı veya sıralı olmayan bir dizide, aranan değere sahip elemanı bulmak için dizinin en başından başlayarak her elemanı sırayla kontrol eder. Aranılan değer bulunduğunda, ilgili elemanın dizideki konumu (indisi) döndürülür. Dizi elemanları sıralı olmadığından, aranan değer dizinin herhangi bir yerinde bulunabilir. Bu yöntemin ortalama karmaşıklığı, dizinin yarısını tarama gerektirmesi nedeniyle daha düşüktür.

```c
#include <stdio.h>

int main() {
    int aranan, i, bulundu=0;
    int dizi[12]={3, 15, 2, 8, 7, 1, 14, 38, 10, -2, 61, 5};
    printf("Dizi icinde aramak istediginiz sayiyi giriniz:\n");
    scanf ("%d", &aranan);
    for(i=0; i<12; i++) {
        if(dizi[i]==aranan) {
            bulundu = 1;
            break;
        }
    }
    if(bulundu) /* if(bulundu==1) */
        printf("Aranan sayi, dizinin %d. elemanidir.", i+1);
    else
        printf("Aranan eleman bu dizide yoktur.\n");
    return 0;
}
```

### İkili Arama (Binary Search) {#ikiliarama}

İkili arama, çalışması için en önemli ön koşulu *sıralı bir dizi* gerektiren bir arama tekniğidir. Dizi sıralı değilse, önce bir sıralama algoritması ile sıralanmalıdır. Bu teknikte, her adımda aranan değer ile dizinin orta elemanı karşılaştırılır.

*   Eğer aranan değer orta elemana eşitse, arama başarılı olur.
*   Eğer aranan değer orta elemandan küçükse, arama işleminin sol yarısında devam eder.
*   Eğer aranan değer orta elemandan büyükse, arama işleminin sağ yarısında devam eder.

Bu yöntemle, her adımda arama alanı yarıya indirgenir, bu da onu büyük veri kümelerinde çok daha verimli kılar.

**ÖRNEK: Aşağıdaki dizide 55 sayısını arayalım.**

| 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3   | 8   | 10  | 11  | 20  | 50  | 55  | 60  | 65  | 70  | 72  | 90  | 91  | 94  | 96  | 99  |

*   **İlk Adım:** Sol=0, Sağ=15. Orta indis \(\lceil(0+15)/2\rceil = \lceil 7.5 \rceil = 8\). \(array[8] = 65\). Aranan değer (55) < 65. Bu durumda aramaya sol yarıda devam edilir.
*   **İkinci Adım:** Sol=0, Sağ=7. Orta indis \(\lceil(0+7)/2\rceil = \lceil 3.5 \rceil = 4\). \(array[4] = 20\). Aranan değer (55) > 20. Bu durumda aramaya sağ yarıda devam edilir.
*   **Üçüncü Adım:** Sol=5, Sağ=7. Orta indis \(\lceil(5+7)/2\rceil = \lceil 6 \rceil = 6\). \(array[6] = 55\). Aranan değer bulundu.

```c
#include <stdio.h>
#include <math.h>

int main() {
    int array[16] = {3,8,10,11,20,50,55,60,65,70,72,90,91,94,96,99};
    double sol = 0;
    double sag = 15;
    int flag = 0;
    int indis = 0;
    int s;
    printf("Dizi icinde aramak istediginiz sayiyi giriniz:\n");
    scanf ("%d", &s);
    while(sol <= sag){
        indis = ceil(sol+(sag-sol)/2);
        printf("indis: %d \n",indis);
        if(array[indis] == s){
            flag = 1;
            printf("Bulundu: %d \n",indis);
            break;
        }
        else if(array[indis] < s){
            sol = indis+1;
        }
        else{
            sag = indis-1;
        }
    }
    if(flag == 0){
        printf("Bulunamadi!\n");
    }
    return 0;
}
```

## Dizilerde Sıralama {#dizilerdesıralama}

Diziler üzerinde işlem yaparken, elemanları belirli bir düzene sokmak için sıralama algoritmaları kullanılır. Bu algoritmalar genellikle dizinin tüm elemanlarını veya belirli bir alt kümesini karşılaştırmayı ve gerektiğinde yer değiştirmeyi içerir. Genellikle iç içe döngüler kullanılarak gerçekleştirilirler. Bu ders kapsamında iki temel sıralama algoritması ele alınacaktır: Kabarcık Sıralama ve Hızlı Sıralama.

### Kabarcık Sıralama (Bubble Sort) {#kabarcıksıralama}

Kabarcık sıralama, adını, her adımda en büyük (veya en küçük) elemanın dizinin sonuna (veya başına) doğru "kabarcıklanmasından" alır. Algoritma, ardışık iki elemanı karşılaştırır ve eğer yanlış sıradalarsa yerlerini değiştirir. Her tam geçişte, en büyük sıralanmamış eleman doğru konumuna yerleşir.

**Çalışma Mantığı:**

1.  Dizinin başından başlayarak ardışık elemanları karşılaştır.
2.  Eğer ilk eleman ikinci elemandan büyükse, yerlerini değiştir.
3.  Bu işlemi dizinin sonuna kadar tekrar et.
4.  En büyük eleman dizinin sonuna yerleşmiş olur.
5.  Bu işlemi, dizi tamamen sıralanana kadar tekrarla, ancak her adımda kontrol edilen son eleman sayısını bir azalt.

```c
#include <stdio.h>
#include <stdlib.h>

/* Kabarcik Siralamasi (Bubble Sort) */
int main(){
    int son, gecici;
    int dizi[100];
    int i,j;
    printf("Girilecek sayi adedi:\n ");
    scanf("%d", &son);
    for(i=0; i<son; i++){
        printf("%d. Sayiyi giriniz: ", i+1);
        scanf("%d", &dizi[i]); }
    printf("Girdiginiz dizi:\n");
    for(i=0; i<son; i++)
        printf("%d ", dizi[i]);
    printf("\n\n");

    // Kabarcik Siralamasi Uygulamasi
    for(i=0; i<son; i++){
        for(j=0; j<son-1-i; j++){
            // Karsilastirma ve Yer Degistirme
            if(dizi[j] > dizi[j+1]) {
                gecici = dizi[j];
                dizi[j] = dizi[j+1];
                dizi[j+1] = gecici;
            }
        }
    }
    printf("Siralanmis dizi:\n");
    for(i=0; i<son; i++)
        printf("%d ", dizi[i]);
    printf("\n");
    return 0;
}
```

### Hızlı Sıralama (Quick Sort) {#hızlısıralama}

Hızlı sıralama, "böl ve yönet" prensibine dayanan, oldukça verimli bir sıralama algoritmasıdır. C standart kütüphanesinde `qsort()` fonksiyonu olarak mevcuttur. Temel olarak bir "pivot" eleman seçilir ve dizi, pivot elemanına göre iki alt diziye ayrılır. Pivot'tan küçük elemanlar sol tarafa, büyük elemanlar ise sağ tarafa yerleştirilir. Bu işlem, tüm dizi sıralanana kadar özyinelemeli olarak devam eder.

**Genel İşleyiş:**

1.  Diziden bir *pivot* eleman seçilir (genellikle ilk eleman).
2.  Dizi, pivot elemanına göre yeniden düzenlenir: Pivot'tan küçük elemanlar soluna, büyük elemanlar sağına yerleştirilir. Bu adımdan sonra pivot elemanı doğru sıralanmış konumundadır.
3.  Sol ve sağ alt diziler için bu işlem özyinelemeli olarak tekrarlanır.

Genellikle, bu algoritmanın karmaşıklığı \(O(n \log n)\) civarındadır.

## Ödev Soruları {#ödevsoruları}

### Ödev 1 {#ödev-1}

Türkiye'de belirli bir ay boyunca tahmin edilen günlük en yüksek hava durumu sıcaklıklarını bir diziye aktararak en düşük sıcaklığın kaçıncı gün tespit edildiğini ekrana yazdıran bir C kodu yazınız.

### Ödev 2 {#ödev-2}

Aşağıda Konya iline ait MGM' nin 5 günlük hava tahminleri ve geçmiş yılların ortalama en düşük ve en yüksek sıcaklık değerleri verilmiştir. Matris işlemlerinden yararlanarak, tahmini en düşük ve en yüksek sıcaklık değerlerinin mevsim ortalamalarının ne kadar altında/üstünde olduğunu hesaplayıp bir matris halinde ekrana yazdıran bir C kodu yazınız.

| TARIH    | TAHMIN EDILEN |                                     |           | GEÇMIŞTE GERÇEKLEŞEN                         |           |
| -------- | ------------- | ----------------------------------- | --------- | -------------------------------------------- | --------- |
|          | Hadise        | Sıcaklık (${^{\circ}} \mathrm{C}$) |           | Ortalama Sıcaklık (${^{\circ}} \mathrm{C}$) |           |
|          |               | En Düşük                            | En Yüksek | En Düşük                                     | En Yüksek |
| 20 Nisan |               | 13                                  | 26        | 4,5                                          | 16,7      |
| 21 Nisan |               | 7                                   | 23        | 4,8                                          | 16,5      |
| 22 Nisan |               | 8                                   | 23        | 4,8                                          | 17        |
| 23 Nisan |               | 9                                   | 28        | 4,4                                          | 17,5      |
| 24 Nisan |               | 11                                  | 30        | 5,3                                          | 18,2      |

## Kaynaklar {#kaynaklar}

*   Programlama Sanatı, Algoritmalar, C Dili Uyarlaması, Dr. Rifat ÇÖLKESEN, Papatya Yayıncılık
*   Her Yönüyle C, Tevfik KIZILÖREN, Kodlab
*   https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il=KONYA