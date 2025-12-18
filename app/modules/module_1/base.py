# app/modules/module_1/base.py
from abc import ABC, abstractmethod


class Transport(ABC):
    
# Ulaşım Modülü base class'ı. Bu sınıftan türeyen her araç (Bus, Shuttle, Bike/Scooter) aynı temel kurallara uyar.
    
    def __init__(self, id: int, kapasite: int, mevcut_lokasyon: str, durum: str):
    
        self.__id = None
        self.__kapasite = None
        self.__mevcut_lokasyon = None
        self.__durum = None

        self.id=id
        self.kapasite=kapasite
        self.mevcut_lokasyon=mevcut_lokasyon
        self.durum=durum
    
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value:int):
        if not isinstance(value,int) or value <=0:
            raise ValueError("id pozitif bir int olmalıdır")
        self__id=value
    
    @property
    def kapasite(self):
        return self.__kapasite
    @kapasite.setter
    def kapasite(self,value:int):
        if not isinstance(value,int) or value <= 0:
            raise ValueError("kapasite en az 1 olmalıdır")
        self.__kapasite= value
    
    @property
    def mevcut_lokasyon(self):
        return self.__mevcut_lokasyon
    @mevcut_lokasyon.setter
    def mevcut_lokasyon(self,value:str):
        if not isinstance(value,str) or not value.strip():
            raise ValueError("Mevcut Lokasyon boş olamaz!")
        self.__mevcut_lokasyon=value.strip()

    @property
    def durum(self):
        return self.__durum
    @durum.setter
    def durum(self,value:str):
        if not isinstance(value,str) or not value.strip():
            raise ValueError("Mevcut Lokasyon boş olamaz!")
        self.__durum=value.strip()

    @abstractmethod
    def sefer_baslat(self, hedef_lokasyon: str) -> None:
        pass

    @abstractmethod
    def sefer_bitir(self) -> None:
        pass

    @abstractmethod
    def bos_kapasite_hesapla(self) -> int:
        
        pass

    # ✅ Ortak (abstract olmayan) metot örneği: herkeste aynı çalışır
    def durum_guncelle(self, yeni_durum: str) -> None:
        self.durum = yeni_durum

    # ✅ Ortak bilgi döndüren metot
    def get_info(self) -> str:
        return f"ID: {self.id} | Kapasite: {self.kapasite} | Konum: {self.mevcut_lokasyon} | Durum: {self.durum}"
