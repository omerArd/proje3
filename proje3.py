import nltk
from nltk.corpus import stopwords
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox

# Stopwords verilerini imdirerek etkisiz kelimeleri görüyoruz
nltk.download('stopwords')

class MetinAnalizi:
    def __init__(self, metin):
        self.metin = metin.lower()
        self.kelimeler = self.metin.split()
        # NLTK kütüphanesinden stopwords modülünü kullanarak İngilizce durak kelimeler listesini alır ve bu listeyi bir kümeye dönüştürür.
        self.etkisiz_kelimeler = set(stopwords.words('english'))

    def harf_sayisi(self):
        # metin içindeki harflerin sayısını döndürür
        return sum(c.isalpha() for c in self.metin)

    def kelime_sayisi(self):
        return len(self.kelimeler)

    def etkisiz_kelime_sayisi(self):
        # metin içindeki etkisiz keilmelerin sayısını döndürür
        return sum(kelime in self.etkisiz_kelimeler for kelime in self.kelimeler)

    def en_cok_gecen_kelimeler(self, n=5):
        # metin içinde en çok geçen kelimeleri ve metinde kaç kere geçtiğini döndürür
        kelimeler = [kelime for kelime in self.kelimeler if kelime not in self.etkisiz_kelimeler]
        return Counter(kelimeler).most_common(n)

    def en_az_gecen_kelimeler(self, n=5):
        # metin içinde en az geçen kelimeleri ve metinde kaç kere geçtiğini döndürür
        kelimeler = [kelime for kelime in self.kelimeler if kelime not in self.etkisiz_kelimeler]
        return Counter(kelimeler).most_common()[:-n-1:-1]

    @staticmethod
    def metin_benzerligi(metin1, metin2):
        kelimeler1 = set(metin1.lower().split())
        kelimeler2 = set(metin2.lower().split())
        benzerlik = len(kelimeler1.intersection(kelimeler2)) / len(kelimeler1.union(kelimeler2))
        return benzerlik * 100

    def kelime_ara(self, kelime):
        return kelime.lower() in self.kelimeler

class MetinAnaliziUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Metin Analizi")

        self.metin_alani = tk.Text(self.root, height=40, width=100)
        self.metin_alani.pack()

        self.analiz_butonu = tk.Button(self.root, text="Analiz Et", command=self.metin_analiz_et)
        self.analiz_butonu.pack()

        self.benzerlik_butonu = tk.Button(self.root, text="Metinleri Karşılaştır", command=self.metinleri_karsilastir)
        self.benzerlik_butonu.pack()

        self.arama_girdisi = tk.Entry(self.root)
        self.arama_girdisi.pack()
        self.arama_butonu = tk.Button(self.root, text="Kelime Ara", command=self.kelime_ara)
        self.arama_butonu.pack()

        self.sonuc_etiketi = tk.Label(self.root, text="")
        self.sonuc_etiketi.pack()

    def metin_analiz_et(self):
        metin = self.metin_alani.get("1.0", tk.END)
        analiz = MetinAnalizi(metin)

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

    def metinleri_karsilastir(self):
        dosya1 = filedialog.askopenfilename(title="İlk Metin Dosyasını Seçin")
        dosya2 = filedialog.askopenfilename(title="İkinci Metin Dosyasını Seçin")

        if dosya1 and dosya2:
            with open(dosya1, 'r') as f1, open(dosya2, 'r') as f2:
                metin1 = f1.read()
                metin2 = f2.read()
                benzerlik = MetinAnalizi.metin_benzerligi(metin1, metin2)
                messagebox.showinfo("Benzerlik", f"Metin Benzerliği: %{benzerlik:.2f}")

    def kelime_ara(self):
        kelime = self.arama_girdisi.get()
        metin = self.metin_alani.get("1.0", tk.END)
        analiz = MetinAnalizi(metin)
        bulundu = analiz.kelime_ara(kelime)
        messagebox.showinfo("Arama Sonucu", f"Kelime '{kelime}' bulundu: {bulundu}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MetinAnaliziUygulamasi(root)
    root.mainloop()



