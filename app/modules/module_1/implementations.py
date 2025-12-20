# app/modules/module_1/implementations.py
from app.modules.module_1.base import BaseClass1
from datetime import datetime

class Bus(Transport):
    
# Otobüs subclass'ı. Transport base class'ından türediği için abstract metotları yazmak zorunda.
    def __init__(
        self,
        id: int,
        kapasite: int,
        mevcut_lokasyon: str,
        durum: str,
        hat_no: str,
        dolu_koltuk: int = 0
    ):
        super().__init__(id, kapasite, mevcut_lokasyon, durum)
        self.__hat_no = None
        self.__dolu_koltuk = None

        # Sefer bilgisi (otobüs nereye gidiyor?) 
        self.__hedef_lokasyon = None
        #sefer zamanlama bilgileri
        self.__sefer_baslangic_saati = 6  #sabah 06:00
        self.__sefer_bitis_saati=23  #akşam 23:00
        self.__sefer_araligi_dk = 20

        self.hat_no= hat_no
        self.dolu_koltuk=dolu_koltuk
    
    @property
    def hat_no(self):
        return self.__hat_no
    @hat_no.setter
    def hat_no(self,value:str):
        if not isinstance(value,str) or len(value.strip()) < 2:
            raise ValueError("Hat no boş olamaz ve en az 2 karakter olmalıdır.")
        self.__hat_no = value.strip()

    @property
    def dolu_koltuk(self,):
        return self.__dolu_koltuk
    @dolu_koltuk.setter
    def dolu_koltuk(self,value:int):
        if not isinstance(value,int) or value <0:
            raise ValueError("Dolu koltuk 0 veya daha büyük bir int olmalıdır")
        if value > self.kapasite:
            raise ValueError("Dolu koltuk kapasiteden büyük olamaz.")
        self.__dolu_koltuk=value

    @property
    def hedef_lokasyon(self):
        return self.__hedef_lokasyon
    @hedef_lokasyon.setter
    def hedef_lokasyon(self,value:str):
        if value is None:
            return
        if not isinstance(value,str) or not value.strip():
            raise ValueError("Hedef Lokasyon boş olamaz.")
        self.__hedef_lokasyon=value.strip()

    @property
    def sefer_baslangic_saati(self):                        #sefer saatleri private tutuldu property ile sadece okunabilir yapıldı.
        return self.__sefer_baslangic_saati
    @property
    def sefer_bitis_saati(self):
        return self.__sefer_bitis_saati
    @property
    def sefer_araligi_dk(self):
        return self.__sefer_araligi_dk
    
    def sefer_zamani_mi(self):
        simdi=datetime.now()
        if simdi.hour < self.sefer_baslangic_saati or simdi.hour>= self.sefer_bitis_saati:
            print("Sefer saatleri aralığında değilsiniz (06:00 - 23:00).")
            return 
        if simdi.minute % 20 != 0:
            print("Şu anda planlanan sefer saatine henüz ulaşılamadı.")

    def otomatik_sefer_kontrol(self, hedef_lokasyon: str, simdi: datetime | None = None):
        """
        Servis katmanı bunu periyodik çağırır.
        Sefer zamanı geldiyse ve otobüs boşsa seferi başlatır.
        Başlattıysa True döner, başlamadıysa False.
        """
        # bakımda ise otomatik de başlatmayalım
        if self.durum == "bakimda":
            return False

        # zaten seferdeyse tekrar başlatmasın
        if self.durum == "seferde":
            return False

        # zaman uygun değilse çık
        if not self.sefer_zamani_mi(simdi):
            return False

        # zaman uygunsa sefer başlat
        self.sefer_baslat(hedef_lokasyon)
        return True


    #  Abstract metot override: sefer başlatma
    def sefer_baslat(self, hedef_lokasyon: str) :
        if self.durum == "bakimda":
            print(f"[Bus {self.id}] Bakımda olduğu için sefer başlatılamaz.")
            return
        
        if self.durum == "seferde":
            print(f"[Bus {self.id}] şuan seferde")
            return

        self.hedef_lokasyon = hedef_lokasyon
        self.durum = "seferde"

        print(f"[Bus {self.id}] Sefer başladı | Hat: {self.hat_no} | Hedef: {hedef_lokasyon}")

    #  Abstract metot override: sefer bitirme
    def sefer_bitir(self):
        if self.durum != "seferde":
            print(f"[Bus {self.id}] Şu an seferde değil, bitirilemez.")
            return

        # Sefer bitince otobüs artık hedefte kabul edelim
        if self.hedef_lokasyon is not None:
            self.mevcut_lokasyon = self.hedef_lokasyon

        self.hedef_lokasyon = None
        self.durum = "bos"
        print(f"[Bus {self.id}] Sefer bitti | Yeni konum: {self.mevcut_lokasyon}")

    #  Abstract metot override: boş kapasite hesaplama
    def bos_kapasite_hesapla(self):
        bos = self.kapasite - self.dolu_koltuk
        if bos < 0:
            bos = 0
        return bos

    #  Nesne metodu örneği (nesne metodu)
    def yolcu_bindir(self, sayi: int = 1) :
        if sayi <= 0:
            return False

        if self.bos_kapasite_hesapla() >= sayi:
            self.dolu_koltuk += sayi
            return True
        print("Yeterli boş koltuk olmadığı için yolcu bindirilemedi ")
        return False

    #  Nesne metodu örneği
    def yolcu_indir(self, sayi: int = 1) :
        if sayi <= 0:
            print("İndirilecek yolcu sayısı geçersiz.")
            return
        self.dolu_koltuk -= sayi
        if self.dolu_koltuk < 0:
            self.dolu_koltuk = 0
        print(f"{sayi} yolcu indirildi.Güncel dolu koltuk:{self.dolu_koltuk}")

    def get_info(self):
        return (
            f"Bus | id={self.id} | hat={self.__hat_no} | "
            f"kapasite={self.kapasite} | dolu={self.__dolu_koltuk} | "
            f"saat={self.__sefer_baslangic_saati} - {self.__sefer_bitis_saati}| "
            f"aralık={self.__sefer_araligi_dk}dk | "
            f"durum={self.durum}"
        )

    #  Sınıf metodu örneği (classmethod)
    @classmethod
    def standart_otobus(cls, id: int, hat_no: str, mevcut_lokasyon: str = "Kampüs"):      # Hazır değerlerle hızlıca Bus üretmek için.

        return cls(
            id=id,
            kapasite=40,
            mevcut_lokasyon=mevcut_lokasyon,
            durum="bos",
            hat_no=hat_no,
            dolu_koltuk=0
        )

    # Statik metot örneği (staticmethod)
    @staticmethod
    def hat_kodu_kontrol(hat_no: str) :  #Basit kontrol: boş olmasın ve en az 2 karakter olsun.
        
        return isinstance(hat_no, str) and len(hat_no.strip()) >= 2

    from app.modules.module_1.base import Transport


class Bike(Transport):
    
    def __init__(
        self,
        id: int,
        mevcut_lokasyon: str,
        durum: str,
        bisiklet_tipi: str ,   # "normal" / "elektrikli" gibi
        kirada_mi: bool ,
        
    ):
        # Bisiklet tek kişilik kabul edelim
        super().__init__(id, kapasite=1, mevcut_lokasyon=mevcut_lokasyon, durum=durum)

        # Bike'a özel alanlar
        
        self.__bisiklet_tipi = None
        self.__kirada_mi = None
         # Sefer bilgisi
        self.__hedef_lokasyon = None
        
        self.bisiklet_tipi= bisiklet_tipi
        self.kirada_mi= kirada_mi
        
    @property
    def bisiklet_tipi(self):
        return self.__bisiklet_tipi
    @bisiklet_tipi.setter
    def bisiklet_tipi(self,value:str):
        if value not in {"normal","elektrikli"}:
            raise ValueError("bisiklet 'tipi normal' veya 'elektrikli' olmalı.")
        self.__bisiklet_tipi=value
    
    @property
    def kirada_mi(self):
        return self.__kirada_mi
    @kirada_mi.setter
    def kirada_mi(self,value:bool):
        if not isinstance(value,bool):
            raise ValueError("kirada mi bool olmalı")
        self.__kirada_mi=value

    @property
    def hedef_lokasyon(self):
        return self.__hedef_lokasyon
    @hedef_lokasyon.setter
    def hedef_lokasyon(self,value:str):
        if value is None:
            self.__hedef_lokasyon=None
            return
        if not isinstance(value,str) or not value.strip():
            raise ValueError("Hedef Lokasyon boş olamaz.")
        self.__hedef_lokasyon= value.strip()

    # Abstract metot override: sefer başlatma
    def sefer_baslat(self, hedef_lokasyon: str):
        if self.durum == "bakimda":
            print(f"[Bike {self.id}] Bakımda olduğu için kullanılamaz.")
            return

        if self.kirada_mi:
            print(f"[Bike {self.id}] kirada görünüyor.")
            return

        self.hedef_lokasyon = hedef_lokasyon
        self.durum = "seferde"
        self.kirada_mi = True

        print(f"[Bike {self.id}] Kullanım başladı | Tip: {self.bisiklet_tipi} | Hedef: {hedef_lokasyon}")

    # Abstract metot override: sefer bitirme
    def sefer_bitir(self):
        if self.durum != "seferde":
            print(f"[Bike {self.id}] Şu an kullanımda değil.")
            return

        if self.hedef_lokasyon is not None:
            self.mevcut_lokasyon = self.hedef_lokasyon

        self.hedef_lokasyon = None
        self.durum = "bos"
        self.kirada_mi = False

        print(f"[Bike {self.id}] Kullanım bitti | Yeni konum: {self.mevcut_lokasyon}")

    # Abstract metot override: boş kapasite hesaplama
    def bos_kapasite_hesapla(self):
        if self.kirada_mi:
            return 0
        else:
            return 1

    # Nesne metodu örneği: bakıma al / çıkar                                 #sistem tarafından çağırılır kullanıcıya açık değildir.
    def bakima_al(self):
        if self.durum == "seferde":
            print(f"[Bike {self.id}] Kullanımdayken bakıma alınamaz.")
            return
        self.durum = "bakimda"
        print(f"[Bike {self.id}] Bakıma alındı.")

    def bakimdan_cikar(self):
        if self.durum != "bakimda":
            return
        self.durum = "bos"
        print(f"[Bike {self.id}] Bakımdan çıktı, kullanıma hazır.")

    def get_info(self):
        return (
            f"Bike | id={self.id} |"
            f"Tip={self.__bisiklet_tipi} | "
            f"lokasyon={self.mevcut_lokasyon} | "
            f"kira durumu={self.__kirada_mi} | "
            f"durum={self.durum}"
        )

    # Classmethod örneği: hızlıca bisiklet üret
    @classmethod
    def bisiklet_olustur(cls, id: int, mevcut_lokasyon: str = "Kampüs", tip: str = "normal"):
        return cls(
        id=id,
        mevcut_lokasyon=mevcut_lokasyon,
        durum="bos",
        bisiklet_tipi=tip,
        kirada_mi=False
    )
from __future__ import annotations
from datetime import datetime

from app.modules.module_1.base import BaseClass1

class Shuttle(Transport):
     def __init__(
        self,
        id:int,
        kapasite: int,
        mevcut_lokasyon:str,
        durum:str,
        baslangic_duragi:str,
        bitis_duragi:str,
        dolu_koltuk:int
        ):
        
        sıper().__init__(id,kapasite,mevcut_lokasyon,durum)
        self.__baslangic_duragi = None
        self.__bitis_duragi = None
        self.__dolu_koltuk = None
        self.__hedef_lokasyon = None

        self.__sefer_baslangic_saati = 7
        self.__sefer_bitis_saatii = 22
        self.__sefer_araligi_dk = 15

        self.__baslangic_duragi = baslangic_duragi
        self.__bitis_duragi = bitis_duragi
        self.__dolu_koltuk=dolu_koltuk

@property
def baslangic_duragi(self):
    return self.__baslangic_duragi
@baslangic_duragi.setter
def baslangic_duragi(self,durak):
    if not isinstance(durak,str):
        raise ValueError("Baslangıç durağı metin olmalıdır")
    durak=durak.strip()
    if durak =="":
        raise ValueError("Başlangıç durağı boş olamaz")
    self.__baslangic_duragi = durak

@property
def bitis_duragi(self):
    return self.__bitis_duragi
@bitis_duragi.setter
def bitis_duragi(self,durak):
    if not isinstance(durak,str):
        raise ValueError("Bitiş durağı metin olmalıdır")
    durak=durak.strip()
    if durak=="":
        raise ValueError("Bitiş durağı boş olamaz.")
    
@property
def dolu_koltuk(self):
    return self.__dolu_koltuk 
@dolu_koltuk.setter
def dolu_koltuk(self,sayi):
    if not isinstance(sayi,int):
        raise ValueError("dolu koltuk int olmalıdır.")
    if sayi<0:
        raise ValueError("dolu koltuk negatif olamaz.")
    if sayi>self.kapasite:
        raise ValueError("Kapasite aşılamaz.")
    self.__dolu_koltuk= sayi

@staticmethod
def saat_uygun_mu(baslangic_saat: int, bitis_saat: int) -> bool:
        simdiki_saat = datetime.now().hour
        return baslangic_saat <= simdiki_saat < bitis_saat

def binis_yap(self,kisi_sayisi):
    if not isinstance(kisi_sayisi,int) or kisi_sayisi<=0:
        raise ValueError("kişi sayısı pozitif int olmalıdır.")
    if self.__dolu_koltuk + kisi_sayisi > self.kapasite:
        raise ValueError("Kapasite Aşılamaz.")
    self.__dolu_koltuk += kisi_sayisi

def inis_yap(self,kisi_sayisi):
    if not isinstance(kisi_sayisi,int) or kisi_sayisi<=0:
        raise ValueError("kişi sayısı pozitif int olmalıdır.")
    if self.__dolu_koltuk - kisi_sayisi <0:
        raise ValueError("İnen Kişi sayısı dolu koltuktan fazla olamaz.")
    self.__dolu_koltuk -= kisi_sayisi

def sefer_baslat(self,hedef_lokasyon:str):
    if not Shuttle.saat_uygun_mu(self.__sefer_baslangic_saati , self.__sefer_bitis_saati):
        print( f"[Shuttle {self.id}] Sefer saatleri dışında! (07:00 - 22:00)")
        return
    if self.durum == "bakimda":
        print(f"[Shuttle {self.id}] Bakımda olduğu için sefer başlatılamaz.")
        return

    if self.durum == "seferde":
        print(f"[Shuttle {self.id}] Zaten seferde.")
        return

    if not self.hedef_gecerli_mi(hedef_lokasyon):
        print(
            f"[Shuttle {self.id}] Hedef geçersiz! "
            f"Sadece '{self.__baslangic_duragi}' veya '{self.__bitis_duragi}' olabilir."
        )
        return

    self.__hedef_lokasyon = hedef_lokasyon
    self.durum = "seferde"

    print(
            f"[Shuttle {self.id}] Sefer başladı | "
            f"{self.__baslangic_duragi} <-> {self.__bitis_duragi} | "
            f"Hedef: {hedef_lokasyon} | "
            f"Aralık: {self.__sefer_araligi_dk} dk"
        )
    
def sefer_bitir(self):
        self.durum = "beklemede"
        self.__hedef_lokasyon = None
        print(f"[Shuttle {self.id}] Sefer bitti, beklemede.")

@classmethod
def shuttle_olustur(cls, id: int):
        return cls(
            id=id,
            kapasite=20,
            mevcut_lokasyon="Yurtlar",
            durum="beklemede",
            baslangic_duragi="Yurtlar",
            bitis_duragi="Kampüs",
            dolu_koltuk=0
        )



