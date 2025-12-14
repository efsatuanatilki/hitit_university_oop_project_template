# app/modules/module_1/base.py
from abc import ABC, abstractmethod


class Transport(ABC):
    """
    Ulaşım Modülü base class'ı.
    Bu sınıftan türeyen her araç (Bus, Shuttle, Bike/Scooter) aynı temel kurallara uyar.
    """

    def __init__(self, id: int, kapasite: int, mevcut_lokasyon: str, durum: str):
        # Araç benzersiz id
        self.id = id

        # Araç kapasitesi (otobüs için koltuk sayısı gibi)
        self.kapasite = kapasite

        # Araç şu an nerede?
        self.mevcut_lokasyon = mevcut_lokasyon

        # Durum örn: "bos", "seferde", "bakimda"
        self.durum = durum

    @abstractmethod
    def sefer_baslat(self, hedef_lokasyon: str) -> None:
        """
        Seferi başlatır. Subclass kendi mantığına göre durum/lokasyon vb. yönetir.
        """
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
