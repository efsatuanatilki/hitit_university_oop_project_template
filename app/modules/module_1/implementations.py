# app/modules/module_1/implementations.py
from app.modules.module_1.base import BaseClass1

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
        self.hat_no = hat_no
        self.dolu_koltuk = dolu_koltuk
        # Sefer bilgisi (otobüs nereye gidiyor?) 
        self.hedef_lokasyon = None

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
    def bos_kapasite_hesapla(self) -> int:
        bos = self.kapasite - self.dolu_koltuk
        if bos < 0:
            bos = 0
        return bos

    #  Nesne metodu örneği (nesne metodu)
    def yolcu_bindir(self, sayi: int = 1) -> bool:
        """
        Yolcu bindirmeyi dener.
        Yer yoksa False döner.
        """
        if sayi <= 0:
            return False

        if self.bos_kapasite_hesapla() >= sayi:
            self.dolu_koltuk += sayi
            return True

        return False

    #  Nesne metodu örneği
    def yolcu_indir(self, sayi: int = 1) -> None:
        if sayi <= 0:
            return
        self.dolu_koltuk -= sayi
        if self.dolu_koltuk < 0:
            self.dolu_koltuk = 0

    #  Sınıf metodu örneği (classmethod)
    @classmethod
    def standart_otobus(cls, id: int, hat_no: str, mevcut_lokasyon: str = "Kampüs") -> "Bus":      # Hazır değerlerle hızlıca Bus üretmek için.

        return cls(
            id=id,
            kapasite=40,
            mevcut_lokasyon=mevcut_lokasyon,
            durum="bos",
            hat_no=hat_no,
            dolu_koltuk=0
        )

    # ✅ Statik metot örneği (staticmethod)
    @staticmethod
    def hat_kodu_kontrol(hat_no: str) -> bool:  #Basit kontrol: boş olmasın ve en az 2 karakter olsun.
        
        return isinstance(hat_no, str) and len(hat_no.strip()) >= 2
