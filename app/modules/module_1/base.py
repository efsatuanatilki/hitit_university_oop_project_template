# app/modules/module_1/base.py
from abc import ABC, abstractmethod


class Transport(ABC):
    
# Ulaşım Modülü base class'ı. Bu sınıftan türeyen her araç (Bus, Shuttle, Bike/Scooter) aynı temel kurallara uyar.
    
    def __init__(self, id: int, kapasite: int, mevcut_lokasyon: str, durum: str):
    
        self.id = id
        self.kapasite = kapasite
        self.mevcut_lokasyon = mevcut_lokasyon
        self.durum = durum

    @abstractmethod
    def sefer_baslat(self, hedef_lokasyon: str) -> None:
        pass

    @abstractmethod
    def sefer_bitir(self) -> None:
        """
        Seferi bitirir. Subclass kendi mantığına göre durum günceller.
        """
        pass

    @abstractmethod
    def bos_kapasite_hesapla(self) -> int:
        """
        Araçta kaç kişilik boş yer kaldı? (Subclass kendi verisine göre hesaplar)
        """
        pass

    # ✅ Ortak (abstract olmayan) metot örneği: herkeste aynı çalışır
    def durum_guncelle(self, yeni_durum: str) -> None:
        self.durum = yeni_durum

    # ✅ Ortak bilgi döndüren metot
    def get_info(self) -> str:
        return f"ID: {self.id} | Kapasite: {self.kapasite} | Konum: {self.mevcut_lokasyon} | Durum: {self.durum}"
