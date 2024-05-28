import nltk # Doğal dil işleme kütüphanesi olan NLTK'yi içe aktarma
from nltk.corpus import stopwords # NLTK'nin stopwords modülünü içe aktarma
from collections import Counter # Koleksiyon modülünden Counter sınıfını içe aktarma
import tkinter as tk  # Tkinter kütüphanesini içe GUI için içe aktarma
from tkinter import filedialog, messagebox # Tkinter'dan dosya dialog ve mesaj kutusu modüllerini içe aktarma
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path

# NLTK'nin durak kelimeler listesini indirme (stopwords)
nltk.download('stopwords')

# Türkçe durak kelimeler listesi (stopwords)
turkce_stopwords = set([
    "acaba", "ama", "aslında", "az", "bazı", "belki", "biri", "birkaç", "birçok", "bu", 
    "çünkü", "da", "daha", "de", "defa", "diye", "eğer", "en", "gibi", "hem", "hep", 
    "hepsi", "her", "hiç", "için", "ile", "ise", "kez", "ki", "kim", "mı", "mu", "mü", 
    "nasıl", "ne", "neden", "nerde", "nerede", "nereye", "niçin", "niye", "o", "sanki", 
    "şayet", "şey", "siz", "şu", "tüm", "ve", "veya", "ya", "yani"])

class VeriDepolama:
    def __init__(self, db_name="metin_analizi.db"):
        #self.db_path = Path.home() / "Desktop" / db_name  # Veritabanı dosyasını masaüstünde oluşturur
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.tablo_olustur()

    def tablo_olustur(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Metinler (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metin TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS BenzerlikSonuclari (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metin1_id INTEGER,
                metin2_id INTEGER,
                jaccard REAL,
                cosine REAL,
                FOREIGN KEY(metin1_id) REFERENCES Metinler(id),
                FOREIGN KEY(metin2_id) REFERENCES Metinler(id)
            )
        ''')
        self.conn.commit()

    def metin_ekle(self, metin):
        self.cursor.execute('''
            INSERT INTO Metinler (metin) VALUES (?)
        ''', (metin,))
        self.conn.commit()
        return self.cursor.lastrowid

    def benzerlik_sonucu_ekle(self, metin1_id, metin2_id, jaccard, cosine):
        self.cursor.execute('''
            INSERT INTO BenzerlikSonuclari (metin1_id, metin2_id, jaccard, cosine) VALUES (?, ?, ?, ?)
        ''', (metin1_id, metin2_id, jaccard, cosine))
        self.conn.commit()

    def metinleri_getir(self):
        self.cursor.execute('SELECT * FROM Metinler')
        return self.cursor.fetchall()

    def benzerlik_sonuclari_getir(self):
        self.cursor.execute('SELECT * FROM BenzerlikSonuclari')
        return self.cursor.fetchall()

    def kapat(self):
        self.conn.close()


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

class MetinAnaliziUygulamasi: 
    def __init__(self, root):
        self.root = root
        self.root.title("Metin Analizi") 

        self.veri_depolama = VeriDepolama()  # VeriDepolama sınıfından bir örnek oluşturur

        self.metin_alani = tk.Text(self.root, height=20, width=80)
        self.metin_alani.pack(pady=10)

        self.analiz_butonu = tk.Button(self.root, text="Metin Analiz Et", command=self.metin_analiz_et)
        self.analiz_butonu.pack(pady=5)

        self.benzerlik_butonu_jaccard = tk.Button(self.root, text="Metinleri Karşılaştır (Jaccard)", command=self.metinleri_karsilastir_jaccard)
        self.benzerlik_butonu_jaccard.pack(pady=5)

        self.benzerlik_butonu_cosine = tk.Button(self.root, text="Metinleri Karşılaştır (Cosine)", command=self.metinleri_karsilastir_cosine)
        self.benzerlik_butonu_cosine.pack(pady=5)

        self.arama_girdisi = tk.Entry(self.root)
        self.arama_girdisi.pack(pady=5)
        self.arama_butonu = tk.Button(self.root, text="Kelime Ara", command=self.kelime_ara)
        self.arama_butonu.pack(pady=5)

        self.sonuc_etiketi = tk.Label(self.root, text="", justify="left")
        self.sonuc_etiketi.pack(pady=10)

        self.veri_yonetimi_butonu = tk.Button(self.root, text="Veri Yönetimi", command=self.veri_yonetimi)
        self.veri_yonetimi_butonu.pack(pady=5)

    def metin_analiz_et(self):
        metin = self.metin_alani.get("1.0", tk.END).strip()
        if not metin:
            messagebox.showwarning("Uyarı", "Lütfen analiz edilecek bir metin girin!")
            return

        analiz = MetinAnalizi(metin, dil="tr")
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
        self.sonuc_etiketi.config(text=sonuc)

        metin_id = self.veri_depolama.metin_ekle(metin)  # Metni veritabanına ekler

    def metinleri_karsilastir_jaccard(self):
        dosya1 = filedialog.askopenfilename(title="İlk Metin Dosyasını Seçin")
        dosya2 = filedialog.askopenfilename(title="İkinci Metin Dosyasını Seçin")

        if not dosya1 or not dosya2:
            messagebox.showwarning("Uyarı", "Lütfen karşılaştırmak için iki dosya seçin.")
            return

        with open(dosya1, 'r', encoding='utf-8') as f1, open(dosya2, 'r', encoding='utf-8') as f2:
            metin1 = f1.read()
            metin2 = f2.read()
            benzerlik = MetinAnalizi.metin_benzerligi_jaccard(metin1, metin2)
            messagebox.showinfo("Benzerlik (Jaccard)", f"Metin Benzerliği (Jaccard): %{benzerlik:.2f}")

            metin1_id = self.veri_depolama.metin_ekle(metin1)
            metin2_id = self.veri_depolama.metin_ekle(metin2)
            self.veri_depolama.benzerlik_sonucu_ekle(metin1_id, metin2_id, benzerlik, None)

    def metinleri_karsilastir_cosine(self):
        dosya1 = filedialog.askopenfilename(title="İlk Metin Dosyasını Seçin")
        dosya2 = filedialog.askopenfilename(title="İkinci Metin Dosyasını Seçin")

        if not dosya1 or not dosya2:
            messagebox.showwarning("Uyarı", "Lütfen karşılaştırmak için iki dosya seçin.")
            return

        with open(dosya1, 'r', encoding='utf-8') as f1, open(dosya2, 'r', encoding='utf-8') as f2:
            metin1 = f1.read()
            metin2 = f2.read()
            benzerlik = MetinAnalizi.metin_benzerligi_cosine(metin1, metin2)
            messagebox.showinfo("Benzerlik (Cosine)", f"Metin Benzerliği (Cosine): %{benzerlik:.2f}")

            metin1_id = self.veri_depolama.metin_ekle(metin1)
            metin2_id = self.veri_depolama.metin_ekle(metin2)
            self.veri_depolama.benzerlik_sonucu_ekle(metin1_id, metin2_id, None, benzerlik)

    def kelime_ara(self):
        kelime = self.arama_girdisi.get().strip()
        if not kelime:
            messagebox.showwarning("Uyarı", "Lütfen aramak istediğiniz bir kelime girin.")
            return

        metin = self.metin_alani.get("1.0", tk.END)
        analiz = MetinAnalizi(metin, dil="tr")
        bulundu = analiz.kelime_ara(kelime)
        messagebox.showinfo("Arama Sonucu", f"Kelime '{kelime}' bulundu: {bulundu}")

    def veri_yonetimi(self):
        def verileri_goster():
            metinler = self.veri_depolama.metinleri_getir()
            for metin in metinler:
                tree.insert("", tk.END, values=metin)

        def sonuclari_goster():
            sonuclar = self.veri_depolama.benzerlik_sonuclari_getir()
            for sonuc in sonuclar:
                tree.insert("", tk.END, values=sonuc)

        pencere = tk.Toplevel(self.root)
        pencere.title("Veri Yönetimi")

        tree = ttk.Treeview(pencere, columns=("ID", "Metin"))
        tree.heading("ID", text="ID")
        tree.heading("Metin", text="Metin")
        tree.pack()

        metinleri_goster_butonu = tk.Button(pencere, text="Metinleri Göster", command=verileri_goster)
        metinleri_goster_butonu.pack(pady=5)

        sonuclari_goster_butonu = tk.Button(pencere, text="Sonuçları Göster", command=sonuclari_goster)
        sonuclari_goster_butonu.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = MetinAnaliziUygulamasi(root)
    root.mainloop()