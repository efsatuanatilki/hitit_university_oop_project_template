import pytest

from app.modules.module_1.implementations import Bus, Bike, Shuttle, UlasimServisi
from app.modules.module_1.repository import (
    InMemoryAracRepository,
    InMemoryCuzdanRepository,
    InMemoryBiletRepository,
    InMemoryKiralamaRepository,
)


def make_service():
    arac_repo = InMemoryAracRepository()
    cuzdan_repo = InMemoryCuzdanRepository()
    bilet_repo = InMemoryBiletRepository()
    kiralama_repo = InMemoryKiralamaRepository()
    servis = UlasimServisi(arac_repo, cuzdan_repo, bilet_repo, kiralama_repo)
    return servis, arac_repo, cuzdan_repo, bilet_repo, kiralama_repo


def test_arac_olusturma():
    bus = Bus.standart_otobus(1, "B1")
    shuttle = Shuttle.shuttle_olustur(2)
    bike = Bike.bisiklet_olustur(3)

    assert bus.id == 1
    assert shuttle.id == 2
    assert bike.id == 3


def test_sefer_baslatma():
    servis, arac_repo, *_ = make_service()
    bus = Bus.standart_otobus(1, "B1")
    arac_repo.ekle(bus)

    servis.sefer_baslat(1, "Yurtlar")
    assert bus.durum == "seferde"
    assert bus.hedef_lokasyon == "Yurtlar"


def test_kapasite_siniri_bilet_kes():
    servis, arac_repo, *_ = make_service()
    bus = Bus(id=1, kapasite=2, mevcut_lokasyon="Kampüs", durum="bos", hat_no="B1", dolu_koltuk=2)
    arac_repo.ekle(bus)

    servis.bakiye_yukle("Ali", 100)

    with pytest.raises(ValueError):
        servis.bilet_kes("Ali", 1, "Kampüs", "Yurtlar", kisi_sayisi=1)


def test_repository_kayit_sil():
    _, arac_repo, *_ = make_service()
    bus = Bus.standart_otobus(1, "B1")

    arac_repo.ekle(bus)
    assert arac_repo.id_ile_bul(1) is not None

    assert arac_repo.sil(1) is True
    assert arac_repo.id_ile_bul(1) is None


def test_servis_islev():
    servis, arac_repo, *_ = make_service()

    bus = Bus.standart_otobus(1, "B1")
    bike = Bike.bisiklet_olustur(2)
    arac_repo.ekle(bus)
    arac_repo.ekle(bike)

    servis.bakiye_yukle("Ali", 200)

    biletler = servis.bilet_kes("Ali", 1, "Kampüs", "Yurtlar", kisi_sayisi=2)
    assert len(biletler) == 2
    assert bus.dolu_koltuk == 2

    kayit = servis.bisiklet_kirala("Ali", 2, "Kampüs")
    assert kayit.durum == "Aktif"

    kayit2 = servis.bisiklet_teslim_et("Ali", kayit.id, "Yurtlar")
    assert kayit2.durum == "Bitti"
