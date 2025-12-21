# app/modules/module_1/implementations.py
from app.modules.module_1.base import Transport
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
    
    def sefer_baslatilabilir_mi(self):
        if self.durum=="bakimda":
            return False
        if self.durum=="seferde":
            return False
        return True
    
    def sefer_zamani_mi(self):
        simdi=datetime.now()
        if simdi.hour < self.sefer_baslangic_saati or simdi.hour>= self.sefer_bitis_saati:
            print("Sefer saatleri aralığında değilsiniz (06:00 - 23:00).")
            return False
        if simdi.minute % 20 != 0:
            print("Şu anda planlanan sefer saatine henüz ulaşılamadı.")
            return False
        return True

    def otomatik_sefer_kontrol(self, hedef_lokasyon: str, simdi: datetime | None = None):
    
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
        
        super().__init__(id,kapasite,mevcut_lokasyon,durum)
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

from dataclasses import dataclass
from datetime import datetime
from typing import  Any

class KampusCuzdani:
    def __init__(self,sahip:str,bakiye: float, para_birimi:str ="TRY"):
        self.sahip=sahip
        self.para_birimi=para_birimi
        self._bakiye= 0.0

        self._bakiye_ayarla(bakiye) 

    @property
    def bakiye(self):
        return self._bakiye
    @bakiye.setter
    def bakiye(self,value:float):
        raise AttributeError("Bakiye doğrudan değiştirilemez.")
    
    def _bakiye_ayarla(self,value:float):
        if not isinstance(value,(int,float)):
            raise ValueError("Bakiye sayı olmalı.")
        if float(value) < 0:
            raise ValueError("Bakiye negatif olamaz.")
        self._bakiye = float(value)

    def bakiye_yukle(self,tutar:float):
        if not isinstance(tutar,(int,float)) or float(tutar) <= 0 :
            raise ValueError("Yüklenecek tutar pozitif sayı olmalı.")
        self._bakiye += float(tutar)

    def harca(self,tutar:float):
        if not isinstance(tutar,(int,float)) or float(tutar) <=0 :
            return False
        tutar= float(tutar)
        if self._bakiye>= tutar:
            self._bakiye-=tutar
            return True
        return False
    
    def bilgi(self):
        return f"Kampüs Cüzdanı(sahip={self.sahip}, bakiye={self._bakiye} {self.para_birimi})"

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
    bırakma_noktasi:str| None
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
    def __init__(self,arac_repo:Any, cuzdan_repo:Any,bilet_repo:Any,kiralama_repo:Any):
        self._arac_repo=arac_repo
        self._cuzdan_repo=cuzdan_repo
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
#Bakiye İşlemleri
def bakiye_yukle(self,kullanici:str,tutar:float):
    cuzdan:KampusCuzdani=self._cuzdan_repo.getir_veya_olustur(kullanici)
    return cuzdan.bilgi()

#Bus/Shuttle Bilet kesme(anlık biniş)
def bilet_kes(self,kullanici:str,arac_id:int,binis:str,inis:str):
    arac = self._arac_repo.id_ile_bul(arac_id)
    if arac is None:
        raise ValueError("Araç bulunamadı.")
    #Araç türü
    if "Bus" in arac.__class__.__name__:
        ucret = self.otobus_ucreti()
        arac_turu = "Bus"
    elif "Shuttle" in arac.__class__.__name__:
        ucret= self.shuttle_ucreti()
        arac_turu= "Shuttle"
    else:
        raise ValueError("Bu araç için bilet kesilmez")
    
    #kapasite kontrol
    if arac.dolu_koltuk >= arac.kapasite:
        raise ValueError("Araç dolu.")
    
    #ödeme
    ucret = self.otobus_ucreti()
    cuzdan = self.cuzdan_repo.getir_veya_olustur(kullanici)
    if not cuzdan.harca(ucret):
        raise ValueError("Yetersiz Bakiye.")
    
    arac.dolu_koltuk+=1
    arac.sefer_baslat(inis)

#Bilet kaydı oluştur
    Bilet = Bilet(
            id=self.siradaki_bilet_id,
            kullanici=kullanici,
            arac_id=arac_id,
            arac_turu=arac_turu,
            binis_noktasi=binis,
            inis_noktasi=inis,
            ucret=ucret,
            olusturma_zamani=datetime.now()
    )
    self.siradaki_bilet_id += 1
    self.bilet_repo.ekle(Bilet)
    return Bilet
def bisiklet_kirala(self,kullanici: str, bisiklet_id: int, alma_noktasi: str):
    bisiklet = self.arac_repo.id_ile_bul(bisiklet_id)
    if bisiklet is None:
        raise ValueError("Bisiklet yok.")
    if bisiklet.kirada_mi:
        raise ValueError("Bisiklet şu an kirarda.")
    
    bisiklet.kirada_mi = True
    bisiklet.durum = "Kirada"

    Kayıt= KiralamaKaydi(
        id =self.siradaki_kiralama_id,
        kullanici=kullanici,
        bisiklet_id=bisiklet_id,
        alma_noktasi=alma_noktasi,
        birakma_noktasi=None,
        baslangic_zamani=datetime.now(),
        bitis_zamani= None,
        ucret=0.0,
        durum="Aktif")
    self.siradaki_kiralama_id +=1
    self.kiralama_repo.ekle(Kayıt)
    return Kayıt

def bisiklet_teslim_et(self,kullanici:str,kiralama_id:int,birakma_noktasi:str):
    Kayıt = self.kiralama_repo.id_ile_bul(kiralama_id)
    if Kayıt is None:
        raise ValueError("Kiralama kaydı yok.")
    if Kayıt.durum != "Aktif":
        raise ValueError("Bu kiralama zaten bitmiş.")
    if Kayıt.kullanici != kullanici:
        raise ValueError("Bu kiralama bu kullanıcıya ait değil.")
    #Süre Hesapla
    bitis= datetime.now()
    gecen_saniye = (bitis - Kayıt.baslangic_zamani).total_seconds()
    saat = int(gecen_saniye/3600)

    if gecen_saniye % 3600 != 0 or saat == 0:
        saat +=1
    #ücret
    ucret= saat * self.bisiklet_saatlik_ucret()
    #ödeme
    cuzdan = self.cuzdan_repo.getir_veya_olustur(kullanici)
    if not cuzdan.harca(ucret):
        raise ValueError("Yetersiz bakiye.")
    #kaydı bitir
    Kayıt.bitis_zamani = bitis
    Kayıt.birakma_noktasi=birakma_noktasi
    Kayıt.ucret=float(ucret)
    Kayıt.durum= "Bitti"

    bisiklet = self.arac_repo.id_ile_bul(Kayıt.bisiklet_id)
    bisiklet.kirada_mi = False
    bisiklet.durum = "bos"
    bisiklet.mevcut_lokasyon = birakma_noktasi

    return Kayıt






    
    

        


