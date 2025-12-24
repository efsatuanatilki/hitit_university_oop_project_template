# app/modules/module_1/demo.py
from __future__ import annotations

from datetime import datetime

from app.modules.module_1.implementations import Bus, Shuttle, Bike, UlasimServisi
from app.modules.module_1.repository import (
    InMemoryAracRepository,
    InMemoryBiletRepository,
    InMemoryKiralamaRepository,
)

# =========================
# Basit input yardımcıları
# =========================
def _sep() -> None:
    print("\n" + "=" * 60)

def _pause() -> None:
    input("\nDevam için Enter...")

def _metin_al(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Boş bırakılamaz.")

def _int_al(prompt: str) -> int:
    while True:
        s = input(prompt).strip()
        try:
            return int(s)
        except ValueError:
            print("Sayı gir.")

def _secim_al(prompt: str, secenekler: set[str]) -> str:
    while True:
        s = input(prompt).strip()
        if s in secenekler:
            return s
        print("Geçersiz seçim.")

def _sadece_harf_bosluk_mu(s: str) -> bool:
    # Türkçe karakterler dahil: isalpha() onları da True sayar.
    s = s.strip()
    if not s:
        return False
    for ch in s:
        if ch == " ":
            continue
        if not ch.isalpha():
            return False
    return True

def _isim_soyisim_al() -> str:
    while True:
        ad = input("Ad: ").strip()
        if not _sadece_harf_bosluk_mu(ad):
            print("Sadece harf ve boşluk girilebilir (sayı/işaret yok).")
            continue

        soyad = input("Soyad: ").strip()
        if not _sadece_harf_bosluk_mu(soyad):
            print(" Sadece harf ve boşluk girilebilir (sayı/işaret yok).")
            continue

        # Düzenli gözüksün diye:
        ad = " ".join(ad.split()).title()
        soyad = " ".join(soyad.split()).title()
        return f"{ad} {soyad}"

def _saat_dakika_al(prompt: str = "Sefer saati (HH:MM) (boş=şimdi): ") -> datetime:
    while True:
        s = input(prompt).strip()
        if s == "":
            simdi = datetime.now()
            return simdi.replace(second=0, microsecond=0)

        try:
            saat_str, dakika_str = s.split(":")
            saat = int(saat_str)
            dakika = int(dakika_str)
            if not (0 <= saat <= 23 and 0 <= dakika <= 59):
                raise ValueError

            simdi = datetime.now()
            return simdi.replace(hour=saat, minute=dakika, second=0, microsecond=0)
        except Exception:
            print("Format yanlış. Örn: 07:30 veya 12:45 (ya da boş bırak Enter)")

def _normalize(s: str) -> str:
    return " ".join(s.strip().split()).casefold()

def _durak_sec_case_insensitive(duraklar: list[str], prompt: str) -> str:
    print("Duraklar:", ", ".join(duraklar))

    # normalize -> orijinal durak adı
    mapping = {_normalize(d): d for d in duraklar}

    while True:
        s = _metin_al(prompt)
        key = _normalize(s)
        if key in mapping:
            return mapping[key]
        print("Bu durak listede yok .")

def _bus_durak_sec(bus: Bus, prompt: str) -> str:
    return _durak_sec_case_insensitive(bus.duraklar, prompt)

def _shuttle_durak_sec(prompt: str) -> str:
    return _durak_sec_case_insensitive(Shuttle.DURAKLAR, prompt)

# =========================
# Araçları başlangıçta ekle
# =========================
def _ornek_veri_yukle(arac_repo: InMemoryAracRepository) -> None:
    # Bus'lar
    arac_repo.ekle(Bus.standart_otobus(1, "B1", "Kampüs"))
    arac_repo.ekle(Bus.standart_otobus(2, "B2", "Yurtlar"))

    # Shuttle
    arac_repo.ekle(Shuttle.shuttle_olustur(10))
    arac_repo.ekle(Shuttle.shuttle_olustur(11))

    # Bike (normal/elektrikli)
    arac_repo.ekle(Bike.bisiklet_olustur(100, "Kampüs", "normal"))
    arac_repo.ekle(Bike.bisiklet_olustur(101, "Kampüs", "elektrikli"))
    arac_repo.ekle(Bike.bisiklet_olustur(102, "Yurtlar", "normal"))

def _araclari_yazdir(arac_repo: InMemoryAracRepository) -> None:
    _sep()
    print("Tüm Araçlar")
    for a in arac_repo.listele():
        info = getattr(a, "get_info", None)
        if callable(info):
            print(" -", a.get_info())
        else:
            print(f" - {type(a).__name__} | id={a.id} | durum={a.durum} | lokasyon={a.mevcut_lokasyon}")

# =========================
# Yolcu Ekranları
# =========================
def yolcu_bus(servis: UlasimServisi, arac_repo: InMemoryAracRepository) -> None:
    while True:
        _sep()
        print("YOLCU | BUS")
        print("1) Bilet al")
        print("2) Kapasite hesapla (dolu/boş)")
        print("3) Mevcut seferleri filtreleme")
        print("4) Sefer saati sorgulama (şu an sefer zamanı mı?)")
        print("0) Geri (Katman menüsü)")

        sec = _secim_al("Seçiniz: ", {"1", "2", "3", "4", "0"})
        if sec == "0":
            return

        if sec == "1":
            _sep()
            print(" Yolcu Bilgileri")
            isim = _isim_soyisim_al()

            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Bus ID: ")

            arac = arac_repo.id_ile_bul(arac_id)
            if not isinstance(arac, Bus):
                print("Bu ID bir Bus değil.")
                _pause()
                continue

            binis = _bus_durak_sec(arac, "Başlangıç durağı: ")
            inis = _bus_durak_sec(arac, "Bitiş durağı: ")
            kisi = _int_al("Kişi sayısı: ")

            try:
                biletler, toplam = servis.bilet_kes(isim, arac_id, binis, inis, kisi)
                print(f"Bilet kesildi. Bilet adedi: {len(biletler)} | Toplam: {toplam:.2f} TL")
            except Exception as e:
                print("Hata:", e)

            _pause()

        elif sec == "2":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Bus ID: ")
            try:
                info = servis.kapasite_bilgisi(arac_id)
                print(f"Bus {arac_id} | toplam={info['toplam']} | dolu={info['dolu']} | boş={info['bos']}")
            except Exception as e:
                print("Hata:", e)
            _pause()

        elif sec == "3":
            durum = input("Durum (bos/seferde/bakimda) boş bırak geç: ").strip() or None
            lok = input("Lokasyon (Kampüs/Yurtlar) boş bırak geç: ").strip() or None
            min_bos = input("Min boş koltuk (sayı) boş bırak geç: ").strip()
            min_bos_val = int(min_bos) if min_bos else None

            sonuc = servis.seferleri_filtrele(
                arac_turu="Bus",
                durum=durum,
                lokasyon=lok,
                min_bos_koltuk=min_bos_val,
            )
            print(f"Bulunan Bus sayısı: {len(sonuc)}")
            for a in sonuc:
                print(" -", a.get_info())
            _pause()

        elif sec == "4":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Bus ID: ")
            arac = arac_repo.id_ile_bul(arac_id)
            if not isinstance(arac, Bus):
                print("Bu ID bir Bus değil.")
                _pause()
                continue

            try:
                girilen = _saat_dakika_al("Sefer saati (HH:MM) (boş=şimdi): ")
                uygun = arac.sefer_zamani_mi(girilen)
                print("Şu an sefer zamanı:", "EVET " if uygun else "HAYIR")
            except Exception as e:
                print("Hata:", e)
            _pause()

def yolcu_shuttle(servis: UlasimServisi, arac_repo: InMemoryAracRepository) -> None:
    while True:
        _sep()
        print("YOLCU | SHUTTLE")
        print("1) Bilet al")
        print("2) Kapasite hesapla (dolu/boş)")
        print("3) Mevcut seferleri filtreleme")
        print("4) Sefer saati sorgulama (şu an sefer zamanı mı?)")
        print("0) Geri (Katman menüsü)")

        sec = _secim_al("Seçiniz: ", {"1", "2", "3", "4", "0"})
        if sec == "0":
            return

        if sec == "1":
            _sep()
            print(" Yolcu Bilgileri")
            isim = _isim_soyisim_al()

            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Shuttle ID: ")

            arac = arac_repo.id_ile_bul(arac_id)
            if not isinstance(arac, Shuttle):
                print("Bu ID bir Shuttle değil.")
                _pause()
                continue

            binis = _shuttle_durak_sec("Başlangıç durağı: ")
            inis = _shuttle_durak_sec("Bitiş durağı: ")
            kisi = _int_al("Kişi sayısı: ")

            try:
                biletler, toplam = servis.bilet_kes(isim, arac_id, binis, inis, kisi)
                print(f" Bilet kesildi. Bilet adedi: {len(biletler)} | Toplam: {toplam:.2f} TL")
            except Exception as e:
                print("Hata:", e)

            _pause()

        elif sec == "2":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Shuttle ID: ")
            try:
                info = servis.kapasite_bilgisi(arac_id)
                print(f"Shuttle {arac_id} | toplam={info['toplam']} | dolu={info['dolu']} | boş={info['bos']}")
            except Exception as e:
                print("Hata:", e)
            _pause()

        elif sec == "3":
            durum = input("Durum (beklemede/seferde/bakimda) isteğe bağlı: ").strip() or None
            lok = input("Lokasyon (Kampüs/Yurtlar) isteğe bağlı: ").strip() or None

            sonuc = servis.seferleri_filtrele(
                arac_turu="Shuttle",
                durum=durum,
                lokasyon=lok,
            )

            print(f"Bulunan Shuttle sayısı: {len(sonuc)}")
            for a in sonuc:
                print(" -", a.get_info())
            _pause() 

        elif sec == "4":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Shuttle ID: ")
            arac = arac_repo.id_ile_bul(arac_id)
            if not isinstance(arac, Shuttle):
                print("Bu ID bir Shuttle değil.")
                _pause()
                continue

            try:
                girilen = _saat_dakika_al("Sefer saati (HH:MM) (boş=şimdi): ")
                uygun = arac.sefer_zamani_mi(girilen)
                print("Şu an sefer zamanı:", "EVET " if uygun else "HAYIR")
            except Exception as e:
                print("Hata:", e)
            _pause()

def yolcu_bike(servis: UlasimServisi, arac_repo: InMemoryAracRepository, kiralama_repo: InMemoryKiralamaRepository) -> None:
    while True:
        _sep()
        print("YOLCU | BIKE")
        print("1) Bike kirala")
        print("2) Bike teslim et")
        print("3) Kirada mı? (Bike ID ile)")
        print("0) Geri (Katman menüsü)")

        sec = _secim_al("Seçiniz: ", {"1", "2", "3", "0"})
        if sec == "0":
            return

        if sec == "1":
            _sep()
            print(" Yolcu Bilgileri")
            isim = _isim_soyisim_al()

            bikes = [
                a for a in arac_repo.listele()
                if isinstance(a, Bike) and a.durum == "bos" and (not a.kirada_mi)
            ]
            if not bikes:
                print("Boşta bisiklet yok.")
                _pause()
                continue

            print("Boşta olan bisikletler (id):", [b.id for b in bikes])
            bisiklet_id = _int_al("Seçilen bisiklet id: ")
            baslangic = _metin_al("Başlangıç durağı/noktası: ")

            try:
                kayit = servis.bisiklet_kirala(isim, bisiklet_id, baslangic)
                print("Kiralandı.")
                print("Başlangıç saati:", kayit.baslangic_zamani.strftime("%Y-%m-%d %H:%M:%S"))
            except Exception as e:
                print("Hata:", e)

            _pause()

        elif sec == "2":
            _sep()
            print("Yolcu Bilgileri")
            isim = _isim_soyisim_al()

            bisiklet_id = _int_al("Kiraladığınız bisiklet id: ")
            bitis = _metin_al("Bitiş durağı/noktası: ")

            kayit = kiralama_repo.bisiklet_id_ile_aktif_kiralama_bul(bisiklet_id)
            if kayit is None:
                print("Bu bisiklet için aktif kiralama kaydı yok.")
                _pause()
                continue
            if kayit.kullanici != isim:
                print("Bu kiralama bu kullanıcıya ait değil.")
                _pause()
                continue

            try:
                sonuc = servis.bisiklet_teslim_et(isim, kayit.id, bitis)
                print("Teslim edildi.")
                print("Bitiş saati:", sonuc.bitis_zamani.strftime("%Y-%m-%d %H:%M:%S"))
                print(f"Kullanım ücreti: {sonuc.ucret:.2f} TL")
            except Exception as e:
                print("Hata:", e)

            _pause()

        elif sec == "3":
            bisiklet_id = _int_al("Bike ID: ")
            b = arac_repo.id_ile_bul(bisiklet_id)
            if not isinstance(b, Bike):
                print("Bu ID bir Bike değil.")
            else:
                print(
                    f"Bike {b.id} | kirada_mi={b.kirada_mi} | durum={b.durum} | "
                    f"lokasyon={b.mevcut_lokasyon} | tip={b.bisiklet_tipi}"
                )
            _pause()

# =========================
# Yönetici Ekranları
# =========================
def yonetici_menu(servis: UlasimServisi, arac_repo: InMemoryAracRepository) -> None:
    while True:
        _sep()
        print("YÖNETİCİ")
        print("1) Tüm araçları listele")
        print("2) Araç ekle")
        print("3) Araç sil")
        print("4) Bakıma al / bakımdan çıkar")
        print("0) Geri (Katman menüsü)")

        sec = _secim_al("Seçiniz: ", {"1", "2", "3", "4", "0"})
        if sec == "0":
            return

        if sec == "1":
            _araclari_yazdir(arac_repo)
            _pause()

        elif sec == "2":
            _sep()
            print("Araç türü:")
            print("1) Bus")
            print("2) Shuttle")
            print("3) Bike")
            t = _secim_al("Seçiniz: ", {"1", "2", "3"})

            try:
                if t == "1":
                    arac_id = _int_al("Bus id: ")
                    hat = _metin_al("Hat no: ")
                    lok = _metin_al("Mevcut lokasyon (Kampüs/Yurtlar vb.): ")
                    bus = Bus.standart_otobus(arac_id, hat, lok)
                    servis.arac_ekle(bus)
                    print("Bus eklendi.")

                elif t == "2":
                    arac_id = _int_al("Shuttle id: ")
                    sh = Shuttle.shuttle_olustur(arac_id)
                    servis.arac_ekle(sh)
                    print(" Shuttle eklendi.")

                elif t == "3":
                    arac_id = _int_al("Bike id: ")
                    lok = _metin_al("Mevcut lokasyon: ")
                    tip = _secim_al("Tip (1=normal, 2=elektrikli): ", {"1", "2"})
                    tip_str = "normal" if tip == "1" else "elektrikli"
                    bk = Bike.bisiklet_olustur(arac_id, lok, tip_str)
                    servis.arac_ekle(bk)
                    print("Bike eklendi.")

            except Exception as e:
                print("Hata:", e)

            _pause()

        elif sec == "3":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Silinecek araç id: ")
            ok = arac_repo.sil(arac_id)
            print("Silindi." if ok else "Bulunamadı.")
            _pause()

        elif sec == "4":
            _araclari_yazdir(arac_repo)
            arac_id = _int_al("Araç id: ")
            a = arac_repo.id_ile_bul(arac_id)
            if a is None:
                print("Araç bulunamadı.")
                _pause()
                continue

            print(f"Seçili: {type(a).__name__} | id={a.id} | durum={a.durum}")
            print("1) Bakıma al")
            print("2) Bakımdan çıkar")
            s = _secim_al("Seçiniz: ", {"1", "2"})

            try:
                if isinstance(a, Bike):
                    if s == "1":
                        a.bakima_al()
                    else:
                        a.bakimdan_cikar()
                else:
                    if s == "1":
                        a.durum = "bakimda"
                    else:
                        a.durum = "bos" if isinstance(a, Bus) else "beklemede"

                arac_repo.guncelle(a)
                print("Güncellendi.")
            except Exception as e:
                print("Hata:", e)

            _pause()

# =========================
# Ana menü
# =========================
def main() -> None:
    arac_repo = InMemoryAracRepository()
    bilet_repo = InMemoryBiletRepository()
    kiralama_repo = InMemoryKiralamaRepository()

    servis = UlasimServisi(arac_repo, bilet_repo, kiralama_repo)
    _ornek_veri_yukle(arac_repo)

    while True:
        _sep()
        print("AKILLI KAMPÜS ULAŞIM SİSTEMİ (DEMO)")   
        print("Seçiniz")
        print("1) Bus")
        print("2) Shuttle")
        print("3) Bike (Normal/Elektrikli)")
        print("0) Çıkış")

        tur = _secim_al("Cevap: ", {"1", "2", "3", "0"})
        if tur == "0":
            print("Çıkış yapıldı.")
            return

        #Katman menüsü artık ayrı bir döngü: yolcudan geri gelince buraya döner
        while True:
            _sep()
            print("Katman seç:")
            print("1) Yolcu/Kullanıcı")
            print("2) Servis/Yönetici")
            print("0) Araç seçimine dön")
            kat = _secim_al("Cevap: ", {"1", "2", "0"})

            if kat == "0":
                break  # araç seçimine dön

            if kat == "2":
                yonetici_menu(servis, arac_repo)
                continue  # katman menüsünde kal

            # kat == "1" (Yolcu)
            if tur == "1":
                yolcu_bus(servis, arac_repo)
            elif tur == "2":
                yolcu_shuttle(servis, arac_repo)
            elif tur == "3":
                yolcu_bike(servis, arac_repo, kiralama_repo)
            # yolcudan çıkınca yine katman menüsüne döner

if __name__ == "__main__":
    main()
