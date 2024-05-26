import nltk # Doğal dil işleme kütüphanesi olan NLTK'yi içe aktarma
from nltk.corpus import stopwords # NLTK'nin stopwords modülünü içe aktarma
from collections import Counter # Koleksiyon modülünden Counter sınıfını içe aktarma
import tkinter as tk  # Tkinter kütüphanesini içe GUI için içe aktarma
from tkinter import filedialog, messagebox # Tkinter'dan dosya dialog ve mesaj kutusu modüllerini içe aktarma
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# NLTK'nin durak kelimeler listesini indirme (stopwords)
nltk.download('stopwords')

# Türkçe durak kelimeler listesi (stopwords)
turkce_stopwords = set([
    "acaba", "ama", "aslında", "az", "bazı", "belki", "biri", "birkaç", "birçok", "bu", 
    "çünkü", "da", "daha", "de", "defa", "diye", "eğer", "en", "gibi", "hem", "hep", 
    "hepsi", "her", "hiç", "için", "ile", "ise", "kez", "ki", "kim", "mı", "mu", "mü", 
    "nasıl", "ne", "neden", "nerde", "nerede", "nereye", "niçin", "niye", "o", "sanki", 
    "şayet", "şey", "siz", "şu", "tüm", "ve", "veya", "ya", "yani"])

class MetinAnalizi:
    def __init__(self, metin, dil="tr"):
        self.metin = metin.lower() # Girilen metni küçük harflere dönüştürür.
        self.kelimeler = self.metin.split() # Metni boşluklara göre bölerek kelimeleri bulma amaçlanır
        
        if dil == "tr":
            self.etkisiz_kelimeler = turkce_stopwords # Eğer dil Türkçe ise, Türkçe etkisiz kelimeler kullanılır
        else:
            self.etkisiz_kelimeler = set(stopwords.words(dil)) # Dil Türkçe değilse NLTK'nin etkisiz kelimeleri kullanılır

    def harf_sayisi(self): # Metindeki harflerin sayısını hesaplayan fonksiyon
        harf_sayisi = 0
        for c in self.metin:
            if c.isalpha():
                harf_sayisi += 1
        return harf_sayisi

    def kelime_sayisi(self): # Metindeki kelime sayısını hesaplayan fonksiyon
        kelime_sayisi = len(self.kelimeler)
        return kelime_sayisi

    def etkisiz_kelime_sayisi(self): # Metindeki etkisiz kelime sayısını hesaplayan fonksiyon
        etkisiz_kelime_sayisi = 0
        for kelime in self.kelimeler:
            if kelime in self.etkisiz_kelimeler:
                etkisiz_kelime_sayisi += 1
        return etkisiz_kelime_sayisi

    def en_cok_gecen_kelimeler(self, n=5): # Metinde en çok geçen kelimeleri döndürür
        kelimeler = []
        for kelime in self.kelimeler:
            if kelime not in self.etkisiz_kelimeler:
                kelimeler.append(kelime)
        en_cok_gecenler = Counter(kelimeler).most_common(n)
        ''' most_common(n) yöntemi, collections modülündeki Counter sınıfının bir parçasıdır. 
             Öğelerden en sık tekrar eden n tanesini döndürür. Bu yöntem, öğeleri tekrar sayılarına 
             göre azalan sırayla sıralar ve en sık görülen n öğeyi bir liste olarak verir.'''
        return en_cok_gecenler

    def en_az_gecen_kelimeler(self, n=5): # Metinde en az geçen kelimeleri döndürür
        kelimeler = []
        for kelime in self.kelimeler:
            if kelime not in self.etkisiz_kelimeler:
                kelimeler.append(kelime)
        en_az_gecenler = Counter(kelimeler).most_common()[:-n-1:-1]
        return en_az_gecenler

    @staticmethod # Statik metot tanımlaması, bu metot sınıf örneği gerektirmez
    def metin_benzerligi_jaccard(metin1, metin2):
        ''' set(), Python'da bir veri yapısıdır ve bir küme oluşturur. Küme, benzersiz elemanları
            içeren bir koleksiyondur. Her bir eleman yalnızca bir kez bulunabilir ve küme içindeki 
            elemanlar sırasızdır.'''
        kelimeler1 = set(metin1.lower().split()) # Birinci metni küçük harflere çevirip kelimelere böler ve set yapar
        kelimeler2 = set(metin2.lower().split()) # İkinci metni küçük harflere çevirip kelimelere böler ve set yapar
        # intersection() yöntemi, iki kümenin kesişimini (ortak elemanlarını) döndürür
        # union() yöntemi, iki kümenin birleşimini (tüm elemanlarını içeren küme) döndürür
        benzerlik = len(kelimeler1.intersection(kelimeler2)) / len(kelimeler1.union(kelimeler2)) 
        benzerlik_yuzdesi = benzerlik * 100
        return benzerlik_yuzdesi

    @staticmethod
    def metin_benzerligi_cosine(metin1, metin2):
        vectorizer = CountVectorizer().fit_transform([metin1, metin2])
        vectors = vectorizer.toarray()
        csim = cosine_similarity(vectors)
        benzerlik_yuzdesi = csim[0][1] * 100
        return benzerlik_yuzdesi

    def kelime_ara(self, kelime): # Metinde kelime arama fonksiyonu
        aranan_kelime = kelime.lower()
        bulundu = False
        for k in self.kelimeler:
            if k == aranan_kelime:
                bulundu = True
                break
        return bulundu

class MetinAnaliziUygulamasi: # Sınıfın başlatıcısı, kök Tkinter penceresini alır
    def __init__(self, root):
        self.root = root
        self.root.title("Metin Analizi") # Pencere başlığını belirler

        self.metin_alani = tk.Text(self.root, height=20, width=80) # Metin alanı widget'ını oluşturur
        self.metin_alani.pack(pady=10) # Metin alanını yerleştirir ve biraz boşluk bırakır

        self.analiz_butonu = tk.Button(self.root, text="Metin Analiz Et", command=self.metin_analiz_et) # Analiz butonunu oluşturur
        self.analiz_butonu.pack(pady=5) # Analiz butonunu yerleştirir ve biraz boşluk bırakır

        self.benzerlik_butonu_jaccard = tk.Button(self.root, text="Metinleri Karşılaştır (Jaccard)", command=self.metinleri_karsilastir_jaccard) # Benzerlik butonunu oluşturur
        self.benzerlik_butonu_jaccard.pack(pady=5) # Benzerlik butonunu yerleştirir ve biraz boşluk bırakır
        
        self.benzerlik_butonu_cosine = tk.Button(self.root, text="Metinleri Karşılaştır (Cosine)", command=self.metinleri_karsilastir_cosine) # Cosine benzerlik butonunu oluşturur
        self.benzerlik_butonu_cosine.pack(pady=5) # Cosine benzerlik butonunu yerleştirir ve biraz boşluk bırakır

        self.arama_girdisi = tk.Entry(self.root) # Kelime arama girişi widget'ını oluşturur
        self.arama_girdisi.pack(pady=5) # Arama girişini yerleştirir ve biraz boşluk bırakır
        self.arama_butonu = tk.Button(self.root, text="Kelime Ara", command=self.kelime_ara) # Arama butonunu oluşturur
        self.arama_butonu.pack(pady=5) # Arama butonunu yerleştirir ve biraz boşluk bırakır

        self.sonuc_etiketi = tk.Label(self.root, text="", justify="left") # Sonuçları gösterecek etiket widget'ını oluşturur
        self.sonuc_etiketi.pack(pady=10) # Sonuç etiketini yerleştirir ve biraz boşluk bırakır

    def metin_analiz_et(self): # Metin analizini yapan fonksiyon
        metin = self.metin_alani.get("1.0", tk.END).strip() # Metin alanındaki metni alır, baştaki ve sondaki boşlukları temizler
        # Eğer metin boşsa uyarı mesajı gönderilir
        if not metin:
            messagebox.showwarning("Uyarı", "Lütfen analiz edilecek bir metin girin!")
            return

        analiz = MetinAnalizi(metin, dil="tr") # MetinAnalizi sınıfından bir örnek oluşturur.

        harf_sayisi = analiz.harf_sayisi()
        kelime_sayisi = analiz.kelime_sayisi()
        etkisiz_kelime_sayisi = analiz.etkisiz_kelime_sayisi()
        en_cok_gecenler = analiz.en_cok_gecen_kelimeler()
        en_az_gecenler = analiz.en_az_gecen_kelimeler()

        sonuc = (f"Harf Sayısı: {harf_sayisi}\n"
                 f"Kelime Sayısı: {kelime_sayisi}\n"
                 f"Etkisiz Kelime Sayısı: {etkisiz_kelime_sayisi}\n"
                 f"En Çok Geçen Kelimeler: {en_cok_gecenler}\n"
                 f"En Az Geçen Kelimeler: {en_az_gecenler}")
        self.sonuc_etiketi.config(text=sonuc) # Sonuç etiketini güncelleme

    def metinleri_karsilastir_jaccard(self): # İki metni karşılaştıran fonksiyon (Jaccard)
        dosya1 = filedialog.askopenfilename(title="İlk Metin Dosyasını Seçin") # İlk metin için dosya seçme diyalogunu açar
        dosya2 = filedialog.askopenfilename(title="İkinci Metin Dosyasını Seçin") # İkinci metin için dosya seçme diyalogunu açar

        if not dosya1 or not dosya2: # Eğer dosyalar seçilmezse uyarı mesajı gönderilir
            messagebox.showwarning("Uyarı", "Lütfen karşılaştırmak için iki dosya seçin.")
            return

        # Dosyaların içeriği okunur   
        with open(dosya1, 'r', encoding='utf-8') as f1, open(dosya2, 'r', encoding='utf-8') as f2:
            metin1 = f1.read()
            metin2 = f2.read()
            benzerlik = MetinAnalizi.metin_benzerligi_jaccard(metin1, metin2) # Metin benzerliği hesaplanır
            messagebox.showinfo("Benzerlik (Jaccard)", f"Metin Benzerliği (Jaccard): %{benzerlik:.2f}")

    def metinleri_karsilastir_cosine(self): # İki metni karşılaştıran fonksiyon (Cosine)
        dosya1 = filedialog.askopenfilename(title="İlk Metin Dosyasını Seçin") # İlk metin için dosya seçme diyalogunu açar
        dosya2 = filedialog.askopenfilename(title="İkinci Metin Dosyasını Seçin") # İkinci metin için dosya seçme diyalogunu açar

        if not dosya1 or not dosya2: # Eğer dosyalar seçilmezse uyarı mesajı gönderilir
            messagebox.showwarning("Uyarı", "Lütfen karşılaştırmak için iki dosya seçin.")
            return

        # Dosyaların içeriği okunur   
        with open(dosya1, 'r', encoding='utf-8') as f1, open(dosya2, 'r', encoding='utf-8') as f2:
            metin1 = f1.read()
            metin2 = f2.read()
            benzerlik = MetinAnalizi.metin_benzerligi_cosine(metin1, metin2) # Metin benzerliği hesaplanır
            messagebox.showinfo("Benzerlik (Cosine)", f"Metin Benzerliği (Cosine): %{benzerlik:.2f}")

    def kelime_ara(self):
        kelime = self.arama_girdisi.get().strip() # Arama girişinden kelimeyi alarak baştaki ve sondaki boşlukları temizler
        if not kelime:
            messagebox.showwarning("Uyarı", "Lütfen aramak istediğiniz bir kelime girin.")
            return

        metin = self.metin_alani.get("1.0", tk.END) # Metin alanından metni alır
        analiz = MetinAnalizi(metin, dil="tr") # MetinAnalizi sınıfından bir örnek oluşturur
        bulundu = analiz.kelime_ara(kelime) # Kelime kontrolü yapar
        messagebox.showinfo("Arama Sonucu", f"Kelime '{kelime}' bulundu: {bulundu}") # Bilgi mesajı verilir

if __name__ == "__main__":
    root = tk.Tk() # Tkinter ana penceresi oluşturulur
    app = MetinAnaliziUygulamasi(root)
    root.mainloop() # Tkinter ana döngüsü başlatılır