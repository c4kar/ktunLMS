##### BILGISAYAR PROGRAMLAMA 1

## Ders Notu 7 - Diziler ve Matrisler

Konya Teknik Üniversitesi
Elektrik - Elektronik Mühendisliği Bölümü
18.04.2024
Konya

# Diziler (Arrays)

- Bugüne kadar anlatılan konularda verileri depolamak için çeşitli değişkenler kullanıldı.
  
  Bazı programlarda aynı tip ve çok fazla sayıda değişkeni depolamak gerekebilir.
  
      Örnek:
      Bir elektrik sinyalinin voltaj değerini 5'er saniye aralıklarla 500 saniye boyunca kaydetmek.
  
  - Böyle bir program yazmak için 100 adet double tipinde değişken tanımlamamız gerekirdi.
    
    - Diziler bu noktada işimizi kolaylaştırmaktadır.
      
      $$
      a=\left\{a_{0}, a_{1}, a_{2}, \ldots, a_{99}\right\}
      $$
      
      # Tanım ve Özellikler

      Dizinin tanımı:
    
      - Bir dizi belirli sayıda ve benzer tipteki değişkenlere tek bir isim ve çeşitli indisler yardımıyla erişim sağlayan özel bir veri yapısıdır.
          Özellikleri:
          - Bir dizi aynı tip verilere sahiptir.
          - Bellekte art arda saklanırlar.

```c
int a[]={1123,1125,1234,1256,1321};
```

# Dizilerin Özellikleri

- Tek boyutlu ve çok boyutlu olabilirler.

| Boyutlar | Örnek          |     | Adı |
|:-------- |:-------------- |:---:|:--- |
| 1        | 0              | 1   | 2   |
|          | 0              | 1   | 2   |
| 2        | 3              | 4   | 5   |
|          | 6              | 7   | 8   |
| 3        | 0              | 1   | 2   |
|          | 3              | 4   | 5   |
|          | 6              | 7   | 8   |
| N        | N Boyutlu Dizi |     |     |

Adı Vektör Matris

3 Boyutlu Dizi

N Boyutlu Dizi

# Dizilerin Özellikleri

- Bir dizi çok sayıda değişken barındırdığından, bunları birbirinden ayırt etmek için indis adı verilen bilgiler kullanılır.
- Bilgisayar programları basit editörlerle yazılır. O editörler $a_{i}$ simgesindeki gibi alt simge koyamaz. Üstelik, derleyiciler de alt simgeyi anlamaz. O nedenle, alt simge işlevini görmek üzere, indisler köşeli parantez içine yazılır.
- Dolayısıyla, bir dizinin öğeleri aşağıdaki gibi yazılır:

$$
a=\{a[0], a[1], a[2], \ldots, a[99]\}
$$

# Dizilerin Özellikleri

- `[]` operatörünün iki işlevi vardır:
  
  1. array bildirimi için kullanılır. `int a[n];`
  2. arrayin bileşenlerinin sıra numarasını (indis) gösterir.

- Arrayde indisler daima tam sayıdır ve 0'dan başlar.
  
    *n* bileşeni olan arrayin indisleri (*i* = 0, 1, 2, . . . *n* − 1) olur.

![img-0.jpeg](img-0.jpeg)

# Dizilerin Özellikleri

- Diziler tanımlanırken; Dizinin adı, dizinin boyutu, dizi elemanlarının hangi tipte olacağı belirtilir.

|                                                                                                                                 | ogrenci\_notu[0] | 45  | 1. eleman |
|:------------------------------------------------------------------------------------------------------------------------------- |:----------------:|:---:|:---------:|
| `veritipi diziAdi[elemanSayisi];`                                                                                               | ogrenci\_notu[1] | 56  | 2. eleman |
| `int a[n];`                                                                                                                     | ogrenci\_notu[2] | 78  | 3. eleman |
| - Örnek:                                                                                                                        | ogrenci\_notu[3] | 93  | 4. eleman |
| double türündeki 8 adet öğrenci notunu bellekte tutmak için aşağıdaki gibi bir dizi tanımlayabiliriz: `double ogrenci_notu[8];` | ogrenci\_notu[4] | 78  | 5. eleman |
|                                                                                                                                 | ogrenci\_notu[5] | 69  | 6. eleman |
|                                                                                                                                 | ogrenci\_notu[6] | 77  | 7. eleman |
|                                                                                                                                 | ogrenci\_notu[7] | 90  | 8. eleman |

# Dizilerin Özellikleri

- Örnek:
    double türündeki 8 adet öğrenci notunu bellekte tutmak:
    Dizileri kullanmasaydık;

```c
double ogrenci_notu1;
double ogrenci_notu2;
double ogrenci_notu3;
double ogrenci_notu4;
double ogrenci_notu5;
double ogrenci_notu6;
double ogrenci_notu7;
double ogrenci_notu8;
```

# Array Bileşenlerinin Kullanımı:

- İki dizi elemanının toplanıp ekrana basılması:
  `printf( " Sonuc:\%f ", ogrenci_notu[0] + ogrenci_notu[1]);`
- Dizinin yedinci elemanının değerinin 2'ye bölünüp x değişkenine atanması: ?
  $\mathrm{x}=$ ogrenci\_notu[6]/2;

・ Dizinin yedinci elemanı: ogrenci\_notu[6]

- Dizinin yedi numaralı elemanı: ogrenci\_notu[7]

# Dizilerde Atama ve Döngii Kurma

- Bir dizinin uzunluğu belirtilmeden de başlangıç değeri atamak mümkündür.
  
    Örnek:
  
  - `int a[]={100,200,300,400};`
  - `float v[]={9.8,11.0,7.5,0.0,12.5};`

- Derleyici bu şekilde bir atama ile karşılaştığında, küme parantezi içindeki eleman sayısını hesaplar ve dizinin o uzunlukta açıldığını varsayar.

- Yukarıdaki örnekte, a dizisinin 4, v dizisinin 5 elemanlı olduğu varsayılır

- `int sayilar[20]={};`

- Tüm dizi elemanlarına 0 değeri atanır...

# Dizier (arrays)

- Örnek:

![img-1.jpeg](img-1.jpeg)
![img-2.jpeg](img-2.jpeg)

Dizinin 1. elemani: 1505608 dir. Dizinin 2. elemani: 0'dir. Dizinin 3. elemani: 164'dir. Dizinin 4. elemani: 0'dir. Dizinin 5. elemani: 4616768 'dir. Dizinin 6. elemani: 0'dir. Dizinin 7. elemani: 1'dir. Dizinin 8. elemani: 0'dir. Dizinin 9. elemani: -1'dir. Dizinin 10. elemani: -1'dir. Dizinin 11. elemani: 164'dir. Dizinin 12. elemani: 0'dir. Dizinin 13. elemani: 1'dir. Dizinin 14. elemani: 0'dir. Dizinin 15. elemani: 4203641'dir. Dizinin 16. elemani: 0'dir. Dizinin 17. elemani: 3'dir. Dizinin 18. elemani: 0'dir. Dizinin 19. elemani: 164'dir. Dizinin 20. elemani: 0'dir.

Dizinin 1. elemani: 0'dir. Dizinin 2. elemani: 0'dir. Dizinin 3. elemani: 0'dir. Dizinin 4. elemani: 0'dir. Dizinin 5. elemani: 0'dir. Dizinin 6. elemani: 0'dir. Dizinin 7. elemani: 0'dir. Dizinin 8. elemani: 0'dir. Dizinin 9. elemani: 0'dir. Dizinin 10. elemani: 0'dir. Dizinin 11. elemani: 0'dir. Dizinin 12. elemani: 0'dir. Dizinin 13. elemani: 0'dir. Dizinin 14. elemani: 0'dir. Dizinin 15. elemani: 0'dir. Dizinin 16. elemani: 0'dir. Dizinin 17. elemani: 0'dir. Dizinin 18. elemani: 0'dir. Dizinin 19. elemani: 0'dir. Dizinin 20. elemani: 0'dir.

# Dizilerde Atama ve Döngii Kurma

- Dizilere başlangıç değeri atarken, tüm elemanlara değer vermeden de atama yapmak mümkündür.
  
    Örnek:
  
  - int sayilar[20] $=\{1,2,3\}$;

- Dizinin ilk 3 elemanına 1,2 ve 3 değerleri atanır. 4'ten itibaren olan dizi elemanlarına 0 değeri atanır...

- Sayısal tipteki dizi elemanlarına 0 değeri, metin tipindeki dizi elemanlarına NULL değeri atanır.

# Dizilerde Atama ve Döngii Kurma

```c
#include <stdio.h>
#include <stdlib.h>

int main() {
  int ornek_dizi[5] = {1, 2, 3, 4, 5}; // Diziyi oluşturma
  int i;
  for (i = 0; i < 5; i++) // Dizi elemanlarına değer atama
  {
    ornek_dizi[i] = ornek_dizi[i] * 3;
  }
  for (i = 0; i < 5; i++) {
    printf("Dizinin %d. elemani: %d'dir. \n", i + 1,
           ornek_dizi[i]); // Dizi elemanlarını yazdırma
  }
  return (0);
}
```

| Dizinin 1. elemani: 3'dir.  |
|:--------------------------- |
| Dizinin 2. elemani: 6'dir.  |
| Dizinin 3. elemani: 9'dir.  |
| Dizinin 4. elemani: 12'dir. |
| Dizinin 5. elemani: 15'dir. |

# Dizilerde Atama Örnekleri

```c
int x[5] = {}; // 5 elemanlı sayısal x dizisi oluşturma
int i = 2;
x[0] = 20;             // Geçerli atama
// x[2.3] = 5;          // Geçersiz atama (Yanlış)
x[2 * i - 3] = 3;      // Geçerli atama, x[1] dizi elemanına 3 değerini atar
x[i++];                // Önce x[2] dizi elemanına erişilir daha sonra i
                        // değişkeninin değeri 1 arttırılır.
x[(int)x[1]];          // x[3] dizi elemanına erişilir
```

# Dizi Elemanlarinı Kullanıcidan Okumak

- Klavyeden maksimum 10 tane sayısal değer girilecektir.
- Girilen sayılar bir dizide saklanacaktır.
- Sayı girme işlemi 0 girilene kadar devam edecektir.
- 0 değeri girildiğinde 0 sayısı hariç girilen diğer tüm değerler diziden okunarak ekrana yazdırılacaktır.

```c
#include <stdio.h>
#include <stdlib.h>
int main()
// Kullantcidan sayısal değer okuma
{
  int ornek_dizi[10]; // Diziyi oluşturma
  int i, j;
  for (i = 0; i < 10;
       i++) // Dizi elemanlarina kullantcıdan değer alma
  {
    printf("%d. sayiyi giriniz", i + 1);
    scanf("%d", &ornek_dizi[i]);
    if (ornek_dizi[i] == 0)
      break;
    j = i;
  }
  for (i = 0; i <= j; i++) // Dizi elemanlarinı yazdırma
  {
    printf("%d \n", ornek_dizi[i]);
  }
  return (0);
}
```

```
C:\Users\Kemal\Desktop\C
1. sayiyi giriniz4
2. sayiyi giriniz6
3. sayiyi giriniz8
4. sayiyi giriniz2
5. sayiyi giriniz3
6. sayiyi giriniz4
7. sayiyi giriniz0
}
Process exited after
Press any key to con
```

# Dizilerle ilgili Önemli Hatırlatmalar

- Dizi boyunca döngü kullanırken dizi indisi asla 0'ın altına inmemeli ve her zaman dizideki toplam eleman sayısından az olmalıdır (büyüklük-1).
- Döngü devam şartının bu aralığın dışındaki elemanlara ulaşılmasını engellediğinden emin olmamız gereklidir.
- Dizi sınırlarının dışındaki elemanları kullanmanın yaratacağı hatalar (genelde ciddi hatalardır) sistemden sisteme farklılık gösterir.

# Dizilerin Bazı Dezavantajları

- Dizinin boyu değiştirilemez:
  
    Dizinin boyunu (boyutunu, bileşenlerinin sayısını) ya bildiriminde belirtiriz ya da bileşenlerine ilk değerlerini atayarak belirlemiş oluruz. Her durumda, dizinin boyu başlangıçta kesin belirlenmiş olur.

- Dizinin bileşen değerleri aynı veri tipindendir:
  
    Bazı durumlarda farklı veri tiplerinden oluşan veri koleksiyonlarını işlemek gerekebilir. O zaman, bileşenleri aynı veri tipinden olan dizi yapısı işimize yaramaz. Java, C\#, Python, Ruby gibi yeni nesil diller farklı veri tiplerinden oluşan koleksiyonlarla iş yapmayı sağlayan yapılar getirmişlerdir.

# Çok Boyutlu Diziler

- Bir dizi birden çok boyuta sahip olabilir.
  
    Örneğin iki boyutlu y dizisi şöyle tanımlanabilir: `int y[5][10];`

- İki boyutlu diziler matris olarak adlandırılır.

- İlk boyuta satır, ikinci boyuta sütun denir. y matrisinin eleman sayısı $5 \times 10=50$ 'dir.

# Çok Boyutlu Diziler

| Dizi Çeşidi                     | Genel Bildirimi                              | Örnek                |
|:------------------------------- |:-------------------------------------------- |:-------------------- |
| Tek boyutlu diziler (Vektörler) | `tip dizi_adı[eleman_sayısı]`                | `int veri[10];`      |
| İki boyutlu diziler (Matrisler) | `tip dizi_adı[satır_sayısı][sutun_sayısı]`   | `float mat[5][4];`   |
| Çok boyutlu diziler             | `tip dizi_adı[boyut_1][boyut_2]...[boyut_n]` | `double x[2][4][2];` |

# Çok Boyutlu Diziler

- Çok boyutlu diziler tek boyuta indirgenerek bellekte tutulurlar.

- Tek indisli dizilerde olduğu gibi, çok indisli dizilere de başlangıç değeri vermek mümkündür.
  
    Örneğin 3 satır ve 4 sütunlu ( $3 \times 4=12$ elemanlı) bir x matrisinin elemanları şöyle tanımlanabilir:
  
  - `int x[3][4]={11,34,42,60,72,99,10,50,80,66,21,38};`
  - ```c
    int x[3][4] = {
        11, 34, 42, 60,   /*1.satırelemanları*/
        72, 99, 10, 50,   /*2.satırelemanları*/
        80, 66, 21, 38
    };                    /*3.satırelemanları*/
    ```

# Çok Boyutlu Diziler

![img-3.jpeg](img-3.jpeg)

# Çok Boyutlu Diziler

- `int x[3][4]={11,34,42,60,72,99,10,50,80,66,21,38};`
- `int y[3][4]={ }; => 0 0 0 0`

`0 0 0 0`
`0 0 0 0`

- `y[0][0]=y[0][0]+x[0][0];`
- `y[0][1]=x[0][2]*2;`
- `y[0][3]=5;`

```c
for (i = 0; i < 3; i++) // y dizisini yazdırma
{
  for (j = 0; j < 4; j++) {
    printf("%d ", y[i][j]);
  }
  printf("\n");
}
```

`11 34 42 60`
`22 99 10 50`
`0 0 66 21 30`
`11 0 40 5`
`0 0 0 0`
`0 0 0 0`

Process exited after Press any key to cond

# Matris İşlemleri

Matris Toplama

$$
\left[\begin{array}{ll}
1 & 3 \\
1 & 2
\end{array}\right]+\left[\begin{array}{ll}
7 & 5 \\
2 & 1
\end{array}\right]=\left[\begin{array}{ll}
8 & 8 \\
3 & 3
\end{array}\right]
$$

```c
for (i = 0; i < 2; i++) {
  for (j = 0; j < 2; j++) {
    C[i][j] = A[i][j] + B[i][j];
    printf("%d ", C[i][j]);
  }
  printf("\n");
}
```

# Matris Çarpma

$$
\begin{aligned}
& \left[\begin{array}{cc}
1 & 2 \\
3 & 1
\end{array}\right] \cdot\left[\begin{array}{l}
4 \\
1
\end{array}\right]_{2}^{3}=\left[\begin{array}{cc}
C_{11} & C_{12} \\
C_{21} & C_{22}
\end{array}\right] \\
& c_{11}=1.4+2.1=6 \\
& c_{12}=1.3+2.2=7
\end{aligned}
$$

```c
for (i = 0; i < 2; i++) {
  for (j = 0; j < 2; j++) {
    for (k = 0; k < 2; k++) {
      C[i][j] += A[i][k] * B[k][j];
    }
    printf("%d ", C[i][j]);
  }
  printf("\n");
}
```

# ÖDEV:

# Bir dersi alan 10 öğrencinin vize ve final notlarını dizilerde saklayabilecek bir program tasarlayın. Notların girişini kullanıcıdan isteyerek dizilere kaydedin. Bu notlara göre vize notu \%40, final notu \%60 olacak şekilde her bir öğrencinin yıl sonu puanını, harf karşılığını ve sınıf ortalamasını ekrana yazdırın.

# KAYNAKLAR:

- Programlama Sanatı, Algoritmalar, C Dili Uyarlaması, Dr. Rifat ÇÖLKESEN, Papatya Yayıncılık

- Her Yönüyle C, Tevfik KIZILÖREN, Kodlab

- C Programlama Dili, Dr. Rifat ÇÖLKESEN, Papatya Yayıncılık

- Celal Bayar Üniversitesi, Hasan Ferdi Turgutlu Teknoloji Fakültesi, YZM1105 Ders Notu
  
  ```
  
  ```
