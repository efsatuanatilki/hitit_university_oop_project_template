from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.modules.module_1.base import Transport

class InMemoryAracRepository:
    def __init__(self):
        self._araclar: dict[int, Transport]={}
    
    def ekle(self, arac: Transport):
        if not isinstance(arac,Transport):
            raise ValueError("Araç bir Transport olmalıdır.")
        if arac.id in self._araclar:
            raise ValueError(f"Bu id zaten var: {arac.id}")
        self._araclar[arac.id] = arac

    def sil(self, arac_id: int):
        if arac_id in self._araclar:
            del self._araclar[arac_id]
            return True
        return False

    def id_ile_bul(self, arac_id: int) -> Optional[Transport]:
        return self._araclar.get(arac_id)

    def listele(self) -> list[Transport]:
        return list(self._araclar.values())

    def duruma_gore_listele(self, durum: str) -> list[Transport]:
        if not isinstance(durum, str) or not durum.strip():
            return []
        durum = durum.strip().lower()
        return [a for a in self._araclar.values() if a.durum == durum]

    def bos_kapasiteye_gore_filtrele(self, en_az_bos: int = 1) -> list[Transport]:
        if not isinstance(en_az_bos, int) or en_az_bos < 0:
            en_az_bos = 0
        return [a for a in self._araclar.values() if a.bos_kapasite_hesapla() >= en_az_bos]
    
    def guncelle(self, arac: Transport) -> None:
        if not isinstance(arac, Transport):
            raise ValueError("Araç bir Transport olmalıdır.")
        if arac.id not in self._araclar:
            raise ValueError("Güncellenecek araç bulunamadı.")
        self._araclar[arac.id] = arac

    def turune_gore_listele(self, tur: str) -> list[Transport]:
        if not isinstance(tur, str) or not tur.strip():
            return []

        tur = tur.strip().lower()

        # circular import olmasın diye burada import
        from app.modules.module_1.implementations import Bus, Shuttle, Bike

        sonuc: list[Transport] = []
        for a in self._araclar.values():
            if tur == "bus" and isinstance(a, Bus):
                sonuc.append(a)
            elif tur == "shuttle" and isinstance(a, Shuttle):
                sonuc.append(a)
            elif tur == "bike" and isinstance(a, Bike):
                sonuc.append(a)

        return sonuc
    
class InMemoryBiletRepository:
#kesilen biletleri saklar 
    def __init__(self):
        self._biletler: list[object] = []
    def ekle(self,bilet):
        from app.modules.module_1.implementations import Bilet

        if not isinstance(bilet,Bilet):
            raise ValueError("Bilet bir bilet nesnesi olmalıdır.")   

        if any(getattr(b, "id", None) == bilet.id for b in self._biletler):
            raise ValueError(f"Bu bilet id zaten var: {bilet.id}")

        self._biletler.append(bilet)
    def listele(self):
        return list(self._biletler)
    
    def id_ile_bul(self, bilet_id:int):
        for b in self._biletler:
            if b.id==bilet_id:
                return b
        return None
    
    def kullaniciya_gore_listele(self,kullanici:str):
        if not isinstance(kullanici,str) or not kullanici.strip():
            return[]
        kullanici=kullanici.strip()
        return [b for b in self._biletler if b.kullanici == kullanici]

class InMemoryKiralamaRepository:
    def __init__(self):
        self._kayitlar: list[object]= []
    def ekle(self,kayit):
        from app.modules.module_1.implementations import KiralamaKaydi

        if not isinstance(kayit,KiralamaKaydi):
            raise ValueError("Kayıt bir KiralamaKaydi olmalıdır.")
        if any(getattr(k, "id", None) == kayit.id for k in self._kayitlar):
            raise ValueError(f"Bu kiralama id zaten var: {kayit.id}")
        self._kayitlar.append(kayit)

    def listele(self):
        return list(self._kayitlar)

    def id_ile_bul(self, kayit_id: int):
        for k in self._kayitlar:
            if k.id == kayit_id:
                return k
        return None

    def kullaniciya_gore_listele(self, kullanici: str):
        if not isinstance(kullanici, str) or not kullanici.strip():
            return []
        kullanici = kullanici.strip()
        return [k for k in self._kayitlar if k.kullanici == kullanici]

    def aktif_kiralari_listele(self):
        # Senin kayıtta durum "Aktif"/"Bitti" (büyük harf) — onu baz alıyoruz
        return [k for k in self._kayitlar if k.durum == "Aktif"]

    def bisiklet_id_ile_aktif_kiralama_bul(self, bisiklet_id: int):
        for k in self._kayitlar:
            if k.bisiklet_id == bisiklet_id and k.durum == "Aktif":
                return k
        return None





