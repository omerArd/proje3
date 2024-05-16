import string
from collections import Counter

class MetinIslemleri:
    def __init__(self, dosya_adi):
        self.dosya_adi = dosya_adi

    def metni_oku(self):
        with open(self.dosya_adi, "r", encoding="utf-8") as dosya:
            return dosya.read()

    def metni_temizle(self, metin):
        for noktalama in string.punctuation:
            metin = metin.replace(noktalama, " ")  # Noktalama işaretlerini boşlukla değiştir
        return metin.lower()

    def kelimelere_ayir(self, metin):
        return metin.split()

    def istatistikleri_hesapla(self, kelimeler, etkisiz_kelimeler):
        harf_sayisi = sum(len(kelime) for kelime in kelimeler)
        kelime_sayisi = len(kelimeler)
        etkisiz_kelime_sayisi = len([kelime for kelime in kelimeler if kelime in etkisiz_kelimeler])
        kelime_sayisi_frekans = Counter(kelimeler)
        en_cok_gecenler = kelime_sayisi_frekans.most_common(5)
        en_az_gecenler = kelime_sayisi_frekans.most_common()[:-6:-1]  # Son 5 kelimeyi al, en az geçenler
        return {
            "harf_sayisi": harf_sayisi,
            "kelime_sayisi": kelime_sayisi,
            "etkisiz_kelime_sayisi": etkisiz_kelime_sayisi,
            "en_cok_gecenler": en_cok_gecenler,
            "en_az_gecenler": en_az_gecenler
        }

class NLPProgrami:
    def __init__(self, dosya_adi):
        self.metin_islemleri = MetinIslemleri(dosya_adi)
        self.etkisiz_kelimeler = self.etkisiz_kelimeleri_yukle()

    def etkisiz_kelimeleri_yukle(self):
        return ["bir", "bu", "ve", "şu", "gibi"]  # Örnek olarak bazı etkisiz kelimeler

    def calistir(self):
        metin = self.metin_islemleri.metni_oku()
        temiz_metin = self.metin_islemleri.metni_temizle(metin)
        kelimeler = self.metin_islemleri.kelimelere_ayir(temiz_metin)
        istatistikler = self.metin_islemleri.istatistikleri_hesapla(kelimeler, self.etkisiz_kelimeler)
        self.istatistikleri_yazdir(istatistikler)

    def istatistikleri_yazdir(self, istatistikler):
        print("Harf Sayısı:", istatistikler["harf_sayisi"])
        print("Kelime Sayısı:", istatistikler["kelime_sayisi"])
        print("Etkisiz Kelime Sayısı:", istatistikler["etkisiz_kelime_sayisi"])
        print("En Çok Geçen 5 Kelime:")
        for kelime, sayi in istatistikler["en_cok_gecenler"]:
            print(f"{kelime}: {sayi} kez")
        print("En Az Geçen 5 Kelime:")
        for kelime, sayi in istatistikler["en_az_gecenler"]:
            print(f"{kelime}: {sayi} kez")

def main():
    dosya_adi = "deneme.txt"
    nlp_programi = NLPProgrami(dosya_adi)
    nlp_programi.calistir()

if __name__ == "__main__":
    main()
