# Metin Analizi Uygulaması

Bu Python uygulaması, kullanıcılara metin analizi yapma ve farklı metinleri karşılaştırma imkanı sunar. Uygulama, Türkçe dil desteği ile birlikte çeşitli analiz özelliklerine sahiptir ve sonuçları SQLite veritabanında saklar. Tkinter kullanılarak oluşturulmuş grafiksel kullanıcı arayüzü (GUI) sayesinde kolay bir kullanım sağlar.

## Özellikler

- Metin analizi: Harf sayısı, kelime sayısı, etkisiz kelime sayısı, en çok ve en az geçen kelimeler.
- Jaccard ve Cosine benzerlik ölçütleri kullanılarak metin karşılaştırma.
- Metin içerisinde kelime arama.
- Veritabanında metin ve benzerlik sonuçlarını saklama ve yönetme.

## Gereksinimler

- Python 3.x
- Gerekli Python kütüphaneleri:
  - nltk
  - sklearn
  - numpy
  - tkinter
  - sqlite3

## Kurulum

1. Bu repoyu klonlayın veya zip dosyası olarak indirin.
2. Gerekli Python kütüphanelerini yükleyin:

    ```bash
    pip install nltk sklearn numpy
    ```

3. `nltk` stopwords veri setini indirin:

    ```python
    import nltk
    nltk.download('stopwords')
    ```

## Kullanım

1. Uygulamayı başlatmak için aşağıdaki komutları çalıştırın:

    ```bash
    python metin_analizi_uygulamasi.py
    ```

2. Uygulama açıldıktan sonra:
   - Metin alanına analiz etmek istediğiniz metni girin ve "Metin Analiz Et" butonuna tıklayın.
   - İki metni karşılaştırmak için "Metinleri Karşılaştır (Jaccard)" veya "Metinleri Karşılaştır (Cosine)" butonlarına tıklayın ve dosyaları seçin.
   - Metin içerisinde kelime aramak için arama giriş alanına kelimeyi girin ve "Kelime Ara" butonuna tıklayın.
   - Veritabanında saklanan verileri görüntülemek için "Veri Yönetimi" butonuna tıklayın.

## Sınıflar ve Metotlar

### VeriDepolama

- **__init__(self, db_name="metin_analizi.db")**: Veritabanı bağlantısını oluşturur ve tabloyu oluşturur.
- **tablo_olustur(self)**: Metinler ve BenzerlikSonuclari tablolarını oluşturur.
- **metin_ekle(self, metin)**: Veritabanına metin ekler.
- **benzerlik_sonucu_ekle(self, metin1_id, metin2_id, jaccard, cosine)**: Benzerlik sonuçlarını veritabanına ekler.
- **metinleri_getir(self)**: Veritabanındaki tüm metinleri getirir.
- **benzerlik_sonuclari_getir(self)**: Veritabanındaki tüm benzerlik sonuçlarını getirir.
- **kapat(self)**: Veritabanı bağlantısını kapatır.

### MetinAnalizi

- **__init__(self, metin, dil="tr")**: Metni işler ve diline göre etkisiz kelimeleri ayarlar.
- **harf_sayisi(self)**: Metindeki harf sayısını hesaplar.
- **kelime_sayisi(self)**: Metindeki kelime sayısını hesaplar.
- **etkisiz_kelime_sayisi(self)**: Metindeki etkisiz kelime sayısını hesaplar.
- **en_cok_gecen_kelimeler(self, n=5)**: En çok geçen kelimeleri döndürür.
- **en_az_gecen_kelimeler(self, n=5)**: En az geçen kelimeleri döndürür.
- **metin_benzerligi_jaccard(metin1, metin2)**: Jaccard benzerlik oranını hesaplar.
- **metin_benzerligi_cosine(metin1, metin2)**: Cosine benzerlik oranını hesaplar.
- **kelime_ara(self, kelime)**: Metinde kelime arar.

### MetinAnaliziUygulamasi

- **__init__(self, root)**: GUI bileşenlerini oluşturur ve yerleştirir.
- **metin_analiz_et(self)**: Metni analiz eder ve sonuçları gösterir.
- **metinleri_karsilastir_jaccard(self)**: İki metni Jaccard benzerliği ile karşılaştırır.
- **metinleri_karsilastir_cosine(self)**: İki metni Cosine benzerliği ile karşılaştırır.
- **kelime_ara(self)**: Metinde kelime arar.
- **veri_yonetimi(self)**: Veritabanı yönetimi için yeni bir pencere açar ve verileri gösterir.



Bu proje MIT Lisansı ile lisanslanmıştır.
