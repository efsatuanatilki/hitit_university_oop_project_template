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
        bisiklet_tipi: str = "normal",   # "normal" / "elektrikli" gibi
        kirada_mi: bool = False
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
        if value not in {"noemal","elektrikli"}:
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

        if self.durum == "seferde":
            print(f"[Bike {self.id}] Zaten kullanımda.")
            return

        if self.kirada_mi:
            print(f"[Bike {self.id}] Zaten kirada görünüyor.")
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
        # Bisiklet tek kişilik: kiradaysa 0, değilse 1
        return 0 if self.kirada_mi else 1

    # Nesne metodu örneği: bakıma al / çıkar
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

    # Classmethod örneği: hızlıca bisiklet üret
    @classmethod
    def standart_bisiklet(cls, id: int, mevcut_lokasyon: str = "Kampüs"):
        return cls(
            id=id,
            mevcut_lokasyon=mevcut_lokasyon,
            durum="bos",
            bisiklet_tipi="normal",
            kirada_mi=False
        )

   
