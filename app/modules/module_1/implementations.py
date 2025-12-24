# app/modules/module_1/implementations.py
from app.modules.module_1.base import Transport
from datetime import datetime
from dataclasses import dataclass
from typing import Any

class Bus(Transport):
    
# Otobüs subclass'ı. Transport base class'ından türemiştir.
    def __init__(
        self,
        id: int,
        kapasite: int,
        mevcut_lokasyon: str,
        durum: str,
        hat_no: str,
        dolu_koltuk: int = 0,
        duraklar: list[str] | None= None
    ):
        super().__init__(id, kapasite, mevcut_lokasyon, durum)
        self.__hat_no = None
        self.__dolu_koltuk = None
        
        self.__hedef_lokasyon = None
        if duraklar is None:
            duraklar = ["Kampüs", "Merkez", "Kütüphane","AVM", "Yurtlar"]

        self.__duraklar = []

        #sefer zamanlama bilgileri
        self.__sefer_baslangic_saati = 6  #sabah 06:00
        self.__sefer_bitis_saati=23  #akşam 23:00
        self.__sefer_araligi_dk = 20

        self.duraklar = duraklar
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
    def hedef_lokasyon(self, value: str | None):
        if value is None:
            self.__hedef_lokasyon = None
            return

        if not isinstance(value, str) or not value.strip():
            raise ValueError("Hedef Lokasyon boş olamaz.")

        self.__hedef_lokasyon = value.strip()

    @property
    def duraklar(self):
        return list(self.__duraklar)
    @duraklar.setter
    def duraklar(self, value):
        if not isinstance(value, list) or len(value) < 2:
            raise ValueError("duraklar en az 2 elemanlı bir liste olmalı.")
        temiz = []
        
        for d in value:
            if not isinstance(d, str) or not d.strip():
                raise ValueError("duraklar sadece dolu metinlerden oluşmalı.")
            temiz.append(d.strip())
    
        # rota uçları Kampüs ve Yurtlar olmalı
        if not (
            (temiz[0] == "Kampüs" and temiz[-1] == "Yurtlar")
            or (temiz[0] == "Yurtlar" and temiz[-1] == "Kampüs")
        ):
            raise ValueError("Duraklar 'Kampüs' ve 'Yurtlar' arasında olmalı (uçlar bu iki durak olmalı).")
    
        self.__duraklar = temiz
    
        if self.mevcut_lokasyon not in self.__duraklar:
            self.mevcut_lokasyon = self.__duraklar[0]

    @property
    def sefer_baslangic_saati(self):                        #sefer saatleri private tutuldu property ile sadece okunabilir yapıldı.
        return self.__sefer_baslangic_saati
    @property
    def sefer_bitis_saati(self):
        return self.__sefer_bitis_saati
    @property
    def sefer_araligi_dk(self):
        return self.__sefer_araligi_dk
    
    #Aşağıdaki durumların olup olmadığını kontrol eder aşağıdaki durumlar var ise sefer başlatmak mantıksızdır.
    def sefer_baslatilabilir_mi(self):
        if self.durum=="bakimda":
            return False
        if self.durum=="seferde":
            return False
        return True
    
    #Uygun sefer saatinde olunup olunmadığını kontrol eder
    def sefer_zamani_mi(self, simdi: datetime | None = None) -> bool:
        
        if simdi is None:
            simdi = datetime.now()
    
        if simdi.hour < self.sefer_baslangic_saati or simdi.hour >= self.sefer_bitis_saati:
            print("Sefer saatleri aralığında değilsiniz (06:00 - 23:00).")
            return False
    
        if simdi.minute % self.sefer_araligi_dk != 0:
            print("Şu anda planlanan sefer saatine henüz ulaşılamadı.")
            return False
    
        return True

    #Bütün durumlar kontrol edilir.Hepsi uygunsa sefer otomatik olarak başlatılır.
    def otomatik_sefer_kontrol(self, hedef_lokasyon: str, simdi: datetime | None = None):
    
        if self.durum == "bakimda":
            return False

        if self.durum == "seferde":
            return False

        if not self.sefer_zamani_mi(simdi):
            return False
        
        self.sefer_baslat(hedef_lokasyon)
        return True


    #  Abstract metot override: sefer başlatma
    def sefer_baslat(self, hedef_lokasyon: str):
        self.hedef_lokasyon = hedef_lokasyon
        self.durum = "seferde"
        print(f"[Bus {self.id}] Sefer başladı | Hat: {self.hat_no} | Hedef: {hedef_lokasyon}")

    # Abstract metot override: sefer bitirme
    def sefer_bitir(self):
        if self.durum != "seferde":
            print(f"[Bus {self.id}] Şu an seferde değil, bitirilemez.")
            return

        if self.hedef_lokasyon is not None:
            self.mevcut_lokasyon = self.hedef_lokasyon

        self.hedef_lokasyon = None
        self.durum = "bos"
        print(f"[Bus {self.id}] Sefer bitti | Yeni konum: {self.mevcut_lokasyon}")

    # Durakları ters çevirerek gidiş yönünü değiştirir.
    def rota_ters_cevir(self) -> None:
        self.duraklar = list(reversed(self.duraklar))

        # güvenlik: mevcut lokasyon listede yoksa başa al
        if self.mevcut_lokasyon not in self.duraklar:
            self.mevcut_lokasyon = self.duraklar[0]


    #  Abstract metot override: boş kapasite hesaplama
    def bos_kapasite_hesapla(self):
        bos = self.kapasite - self.dolu_koltuk
        if bos < 0:
            bos = 0
        return bos
    # Yolcu indir/bindir.
    def yolcu_bindir(self, sayi: int = 1) :
        if sayi <= 0:
            return False

        if self.bos_kapasite_hesapla() >= sayi:
            self.dolu_koltuk += sayi
            return True
        print("Yeterli boş koltuk olmadığı için yolcu bindirilemedi ")
        return False

    def yolcu_indir(self, sayi: int = 1) -> bool:
        if sayi <= 0:
            print("İndirilecek yolcu sayısı geçersiz.")
            return False
        if sayi > self.dolu_koltuk:
            print(f"İnen kişi sayısı dolu koltuktan fazla olamaz. Dolu: {self.dolu_koltuk}")
            return False

        self.dolu_koltuk -= sayi
        print(f"{sayi} yolcu indirildi. Güncel dolu koltuk: {self.dolu_koltuk}")
        return True


    def get_info(self):
        return (
            f"Bus | id={self.id} | hat={self.__hat_no} | "
            f"kapasite={self.kapasite} | dolu={self.__dolu_koltuk} | "
            f"saat={self.__sefer_baslangic_saati} - {self.__sefer_bitis_saati}| "
            f"aralık={self.__sefer_araligi_dk}dk | "
            f"durum={self.durum}"
        )

    # Sınıf metodu örneği (classmethod)
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
    #Verilen saat ve dakika sefer planına uygun mu kontrol eder.
    @staticmethod
    def saat_sefere_uygun_mu(saat: int, dakika: int, aralik_dk: int = 20) -> bool:
        
        if saat < 6 or saat >= 23:
            return False
    
        if dakika % aralik_dk != 0:
            return False
    
        return True

class Bike(Transport):
    
    def __init__(
        self,
        id: int,
        mevcut_lokasyon: str,
        durum: str,
        bisiklet_tipi: str ,   # "normal" / "elektrikli" gibi
        kirada_mi: bool 
        
    ):
        super().__init__(id, kapasite=1, mevcut_lokasyon=mevcut_lokasyon, durum=durum)
        
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
    def hedef_lokasyon(self, value: str | None):
        if value is None:
            self.__hedef_lokasyon = None
            return
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Hedef Lokasyon boş olamaz.")
        self.__hedef_lokasyon = value.strip()

    #Bike özel geçerli 3 durum
    @classmethod
    def gecerli_durumlar(cls) -> set[str]:
        return {"bos", "kirada", "bakimda"}

    # Abstract metot override: sefer başlatma
    def sefer_baslat(self, hedef_lokasyon: str):
        if self.durum == "bakimda":
            print(f"[Bike {self.id}] Bakımda olduğu için kullanılamaz.")
            return

        if self.kirada_mi:
            print(f"[Bike {self.id}] kirada görünüyor.")
            return

        self.hedef_lokasyon = hedef_lokasyon
        self.durum = "kirada"
        self.kirada_mi = True

        print(f"[Bike {self.id}] Kullanım başladı | Tip: {self.bisiklet_tipi} | Hedef: {hedef_lokasyon}")

    # Abstract metot override: sefer bitirme
    def sefer_bitir(self):
        if self.durum != "kirada":
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
        if self.durum == "kirada":
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
    @classmethod
    def bisiklet_olustur(cls, id: int, mevcut_lokasyon: str = "Kampüs", tip: str = "normal"):
        return cls(
            id=id,
            mevcut_lokasyon=mevcut_lokasyon,
            durum="bos",
            bisiklet_tipi=tip,
            kirada_mi=False
        )

    #Staticmethod Örneği: maksimum 24 saat kiralanabilir.
    @staticmethod
    def kiralama_suresi_gecerli_mi(saat: int) -> bool:
        return isinstance(saat, int) and 1 <= saat <= 24


class Shuttle(Transport):
    DURAKLAR = ["Yurtlar","Kampüs"]
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
        super().__init__(id,kapasite,mevcut_lokasyon,durum)

        self.__baslangic_duragi = None
        self.__bitis_duragi = None
        self.__dolu_koltuk = None
        self.__hedef_lokasyon = None 

        self.__sefer_baslangic_saati = 7
        self.__sefer_bitis_saati = 22
        self.__sefer_araligi_dk = 15    

        self.baslangic_duragi = baslangic_duragi
        self.bitis_duragi = bitis_duragi
        self.dolu_koltuk=dolu_koltuk  

        if self.baslangic_duragi == self.bitis_duragi:
            raise ValueError("Shuttle başlangıç ve bitiş durakları aynı olamaz.")

         # Shuttle sadece iki durak arasında çalışsın
        if self.mevcut_lokasyon not in self.DURAKLAR:
            raise ValueError(f"Shuttle konumu sadece {self.DURAKLAR} içinde olmalı.")

    # Shuttle ekstra bir durum kullanıyor: beklemede
    @classmethod
    def gecerli_durumlar(cls) -> set[str]:
        return super().gecerli_durumlar() | {"beklemede"}
    
    @property
    def baslangic_duragi(self):
        return self.__baslangic_duragi
    @baslangic_duragi.setter
    def baslangic_duragi(self, durak: str):
        if not self.durak_gecerli_mi(durak):
            raise ValueError(f"Başlangıç durağı sadece {self.DURAKLAR} içinde olmalı.")
        self.__baslangic_duragi = durak.strip()

    @property
    def bitis_duragi(self):
        return self.__bitis_duragi
    @bitis_duragi.setter
    def bitis_duragi(self, durak: str):
        if not self.durak_gecerli_mi(durak):
            raise ValueError(f"Bitiş durağı sadece {self.DURAKLAR} içinde olmalı.")
        self.__bitis_duragi = durak.strip()


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

    #Verilen zaman için shuttle sefer zamanı mı kontrol eder.
    def sefer_zamani_mi(self, simdi: datetime | None = None) -> bool:
        
        if simdi is None:
            simdi = datetime.now()

        if simdi.hour < self.__sefer_baslangic_saati or simdi.hour >= self.__sefer_bitis_saati:
            return False

        if simdi.minute % self.__sefer_araligi_dk != 0:
            return False
        return True
    
    # Shuttle'da şu an kaç boş koltuk kaldığını hesaplar
    def bos_kapasite_hesapla(self) -> int:
        bos_koltuk = self.kapasite - self.dolu_koltuk
        if bos_koltuk < 0:
            return 0
        return bos_koltuk
    
    @property
    def hedef_lokasyon(self):
        return self.__hedef_lokasyon
    @hedef_lokasyon.setter
    def hedef_lokasyon(self, value: str | None):
        if value is None:
            self.__hedef_lokasyon = None
            return
        if not self.durak_gecerli_mi(value):
            raise ValueError(f"Hedef lokasyon sadece {self.DURAKLAR} içinde olmalı.")

        self.__hedef_lokasyon = value.strip()

    @staticmethod
    def saat_uygun_mu(baslangic_saat: int, bitis_saat: int, simdi: datetime | None = None) -> bool:
        if simdi is None:
            simdi = datetime.now()
        return baslangic_saat <= simdi.hour < bitis_saat

    
    def binis_yap(self, kisi_sayisi: int) -> bool:
        if not isinstance(kisi_sayisi, int) or kisi_sayisi <= 0:
            print(" Kişi sayısı pozitif bir sayı olmalıdır.")
            return False

        if self.dolu_koltuk + kisi_sayisi > self.kapasite:
            print(" Kapasite aşılamaz.")
            return False

        self.dolu_koltuk += kisi_sayisi
        print(f"{kisi_sayisi} kişi bindi. Dolu koltuk: {self.dolu_koltuk}")
        return True

    def inis_yap(self, kisi_sayisi: int) -> bool:
        if not isinstance(kisi_sayisi, int) or kisi_sayisi <= 0:
            print("Kişi sayısı pozitif bir sayı olmalıdır.")
            return False

        if self.dolu_koltuk - kisi_sayisi < 0:
            print("İnen kişi sayısı dolu koltuktan fazla olamaz.")
            return False

        self.dolu_koltuk -= kisi_sayisi
        print(f" {kisi_sayisi} kişi indi. Dolu koltuk: {self.dolu_koltuk}")
        return True

    
    def sefer_baslat(self, hedef_lokasyon: str):
        if self.durum == "bakimda":
            print(f"[Shuttle {self.id}] Bakımda olduğu için sefer başlatılamaz.")
            return
        if self.durum == "seferde":
            print(f"[Shuttle {self.id}] Zaten seferde.")
            return

        self.hedef_lokasyon = hedef_lokasyon
        self.durum = "seferde"
        print(f"[Shuttle {self.id}] Sefer başladı | Hedef: {hedef_lokasyon}")


    def sefer_bitir(self):
        if self.durum != "seferde":
            print(f"[Shuttle {self.id}] Şu an seferde değil.")
            return

        if self.hedef_lokasyon is not None:
            self.mevcut_lokasyon = self.hedef_lokasyon

        self.hedef_lokasyon = None
        self.durum = "beklemede"
        print(f"[Shuttle {self.id}] Sefer bitti | Yeni konum: {self.mevcut_lokasyon}")

    def rota_ters_cevir(self) -> None:
    
        self.baslangic_duragi, self.bitis_duragi = self.bitis_duragi, self.baslangic_duragi

        # bir sonraki sefer için hedefi hazırla 
        self.hedef_lokasyon = self.bitis_duragi

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
    #durak geçerli mi?
    @staticmethod
    def durak_gecerli_mi(durak: str) -> bool:
        return isinstance(durak, str) and durak.strip() in {"Yurtlar", "Kampüs"}


@dataclass
class Bilet:
    id:int
    kullanici:str
    arac_id:int
    arac_turu:str #bus/shuttle
    binis_noktasi:str
    inis_noktasi:str
    ucret: float
    olusturma_zamani: datetime
    
    def bilgi(self):
        return(f"Bilet(id={self.id},kullanıcı={self.kullanici},arac_id={self.arac_id}"
        f"Tür={self.arac_turu}, {self.binis_noktasi}->{self.inis_noktasi}, ucret={self.ucret})")
    
@dataclass
class KiralamaKaydi:
    id:int
    kullanici:str
    bisiklet_id:int
    alma_noktasi:str
    birakma_noktasi:str| None
    baslangic_zamani: datetime
    bitis_zamani: datetime|None
    ucret:float
    durum:str   #Aktif/Bitti

    def bilgi(self):
        return(
            f"Kiralama(id={self.id},kullanici={self.kullanici},bisiklet_id={self.bisiklet_id})"
            f"Durum={self.durum},ucret={self.ucret}"
        )

#SEVİCE(iş kuralları)
class UlasimServisi:
    """ Kurallar: 
    - Otobüs: 10 TL (tek biniş) 
    - Shuttle: 8 TL (tek biniş) -
      Bisiklet: saatlik 5 TL (ücret teslimde kesilir; süre yukarı yuvarlanır) """
    def __init__(self,arac_repo:Any,bilet_repo:Any,kiralama_repo:Any):
        self._arac_repo=arac_repo
        self._bilet_repo=bilet_repo
        self._kiralama_repo=kiralama_repo

        self._siradaki_bilet_id =1
        self._siradaki_kiralama_id =1
    #Ücretler(static)
    @staticmethod
    def otobus_ucreti():
        return 10.0
    @staticmethod
    def shuttle_ucreti():
        return 8.0
    @staticmethod
    def bisiklet_saatlik_ucret():
        return 5.0
    
    def sefer_baslat(self, arac_id: int, hedef_lokasyon: str):
        arac = self._arac_repo.id_ile_bul(arac_id)
        if arac is None:
            raise ValueError("Araç bulunamadı.")

        if not isinstance(arac, (Bus, Shuttle)):
            raise ValueError("Bu araç için sefer başlatılamaz.")

        if arac.durum in {"bakimda", "seferde"}:
            raise ValueError("Araç şu an sefer başlatamaz.")

        arac.sefer_baslat(hedef_lokasyon)

        if hasattr(self._arac_repo, "guncelle"):
            self._arac_repo.guncelle(arac)

        return arac

    def sefer_bitir(self, arac_id: int):
        arac = self._arac_repo.id_ile_bul(arac_id)
        if arac is None:
            raise ValueError("Araç bulunamadı.")

        if not isinstance(arac, (Bus, Shuttle)):
            raise ValueError("Bu araç için sefer bitirme yok.")

        arac.sefer_bitir()

        # Sefer bitti -> yön değişsin (Bus/Shuttle içinde bu metot varsa)
        if hasattr(arac, "rota_ters_cevir"):
            arac.rota_ters_cevir()

        if hasattr(self._arac_repo, "guncelle"):
            self._arac_repo.guncelle(arac)

        return arac

    def kapasite_bilgisi(self, arac_id: int) -> dict:
        arac = self._arac_repo.id_ile_bul(arac_id)
        if arac is None:
            raise ValueError("Araç bulunamadı.")

        if not isinstance(arac, (Bus, Shuttle)):
            raise ValueError("Bu araçta kapasite hesaplanmaz.")

        dolu = arac.dolu_koltuk
        toplam = arac.kapasite
        bos = toplam - dolu
        oran = (dolu / toplam) if toplam > 0 else 0.0

        return {"arac_id": arac_id, "toplam": toplam, "dolu": dolu, "bos": bos, "doluluk_orani": oran}

    #Bus/Shuttle Bilet kesme(anlık biniş)
    def bilet_kes(self, kullanici: str, arac_id: int, binis: str, inis: str, kisi_sayisi: int = 1):
        arac = self._arac_repo.id_ile_bul(arac_id)
        if arac is None:
            raise ValueError("Araç bulunamadı.")
    
        # kişi sayısı kontrol
        if not isinstance(kisi_sayisi, int) or kisi_sayisi < 1:
            raise ValueError("kisi_sayisi 1 veya daha büyük bir tam sayı olmalı.")
    
        # Araç türü + ücret
        if isinstance(arac, Bus):
            ucret = self.otobus_ucreti()
            arac_turu = "Bus"
        elif isinstance(arac, Shuttle):
            ucret = self.shuttle_ucreti()
            arac_turu = "Shuttle"
        else:
            raise ValueError("Bu araç için bilet kesilmez")
    
        # kapasite kontrol (N kişilik)
        bos_koltuk = arac.kapasite - arac.dolu_koltuk
        if kisi_sayisi > bos_koltuk:
            raise ValueError(f"Araçta yeterli boş koltuk yok. Boş: {bos_koltuk}")
    
        # ödeme (toplam)
        toplam_ucret = ucret * kisi_sayisi
        
        # koltuk güncelle
        arac.dolu_koltuk += kisi_sayisi
    
        # N adet bilet üret
        biletler = []
        simdi = datetime.now()
    
        for _ in range(kisi_sayisi):
            bilet = Bilet(
                id=self._siradaki_bilet_id,
                kullanici=kullanici,
                arac_id=arac_id,
                arac_turu=arac_turu,
                binis_noktasi=binis,
                inis_noktasi=inis,
                ucret=ucret,
                olusturma_zamani=simdi
            )
            self._siradaki_bilet_id += 1
            self._bilet_repo.ekle(bilet)
            biletler.append(bilet)
    
        if hasattr(self._arac_repo, "guncelle"):
            self._arac_repo.guncelle(arac)
        
        return biletler, toplam_ucret

    #Bisiklet Kiralama
    def bisiklet_kirala(self,kullanici: str, bisiklet_id: int, alma_noktasi: str):
        bisiklet = self._arac_repo.id_ile_bul(bisiklet_id)
        if bisiklet is None:
            raise ValueError("Bisiklet yok.")
        if bisiklet.kirada_mi:
            raise ValueError("Bisiklet şu an kirarda.")
        
        bisiklet.kirada_mi = True
        bisiklet.durum = "kirada"
    
        Kayit= KiralamaKaydi(
            id =self._siradaki_kiralama_id,
            kullanici=kullanici,
            bisiklet_id=bisiklet_id,
            alma_noktasi=alma_noktasi,
            birakma_noktasi=None,
            baslangic_zamani=datetime.now(),
            bitis_zamani=None,
            ucret=0.0,
            durum="Aktif")
        self._siradaki_kiralama_id +=1
        self._kiralama_repo.ekle(Kayit)
        return Kayit
    
    def bisiklet_teslim_et(self,kullanici:str,kiralama_id:int,birakma_noktasi:str):
        Kayit = self._kiralama_repo.id_ile_bul(kiralama_id)
        if Kayit is None:
            raise ValueError("Kiralama kaydı yok.")
        if Kayit.durum != "Aktif":
            raise ValueError("Bu kiralama zaten bitmiş.")
        if Kayit.kullanici != kullanici:
            raise ValueError("Bu kiralama bu kullanıcıya ait değil.")
        #Süre Hesapla
        bitis= datetime.now()
        gecen_saniye = (bitis - Kayit.baslangic_zamani).total_seconds()
        saat = int(gecen_saniye/3600)
    
        if gecen_saniye % 3600 != 0 or saat == 0:
            saat +=1
        #ücret
        ucret= saat * self.bisiklet_saatlik_ucret()

        #kaydı bitir
        Kayit.bitis_zamani = bitis
        Kayit.birakma_noktasi=birakma_noktasi
        Kayit.ucret=float(ucret)
        Kayit.durum= "Bitti"
    
        bisiklet = self._arac_repo.id_ile_bul(Kayit.bisiklet_id)
        bisiklet.kirada_mi = False
        bisiklet.durum = "bos"
        bisiklet.mevcut_lokasyon = birakma_noktasi
        if hasattr(self._arac_repo, "guncelle"):
            self._arac_repo.guncelle(bisiklet)

        return Kayit
    def arac_ekle(self, arac):
        if arac is None:
            raise ValueError("Araç boş olamaz.")

        self._arac_repo.ekle(arac)
        return arac

    def seferleri_filtrele(
        self,
        arac_turu: str | None = None,     # "Bus", "Shuttle", "Bike"
        durum: str | None = None,         # "bos", "seferde", "beklemede", "kirada"
        lokasyon: str | None = None,      # "Kampüs", "Yurtlar"
        min_bos_koltuk: int | None = None
    ):

        tum_araclar = self._arac_repo.listele()
        sonuc = []

        for arac in tum_araclar:
            # araç türü filtresi
            if arac_turu is not None:
                if arac_turu == "Bus" and not isinstance(arac, Bus):
                    continue
                if arac_turu == "Shuttle" and not isinstance(arac, Shuttle):
                    continue
                if arac_turu == "Bike" and not isinstance(arac, Bike):
                    continue

            # durum filtresi
            if durum is not None and arac.durum != durum:
                continue

            # lokasyon filtresi
            if lokasyon is not None and arac.mevcut_lokasyon != lokasyon:
                continue

            # boş koltuk filtresi (Bus / Shuttle)
            if min_bos_koltuk is not None:
                if not isinstance(arac, (Bus, Shuttle)):
                    continue
                bos = arac.kapasite - arac.dolu_koltuk
                if bos < min_bos_koltuk:
                    continue


            sonuc.append(arac)

        return sonuc


    
    


    
    

        


