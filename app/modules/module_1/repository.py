from __future__ import annotations

from datetime import datetime
from typing import Optional

from app.modules.module_1.base import Transport
from app.modules.module_1.implementations import(
    Bus,Shuttle,Bike,KampusCuzdani,Bilet,KiralamaKaydi)

class InMemoryAracRepository:
    def __init__(self):
        self._araclar: dict[int, Transport]={}
    
    def ekle(self, arac: Transport):
        if not isinstance(arac,Transport):
            raise ValueError("Araç bir Transport olmalıdır.")
        if arac.id in self._araclar:
            raise ValueError(f"Bu id zaten var: {arac.id}")
        self._araclar[arac.id] = arac
    def sil(self, arac_id: int) -> bool:
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
    def turune_gore_listele(self, tur: str) -> list[Transport]:
         if not isinstance(tur, str) or not tur.strip():
            return []
        
        