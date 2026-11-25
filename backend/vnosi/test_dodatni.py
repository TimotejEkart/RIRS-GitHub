from django.test import SimpleTestCase, TestCase

from dostop.models import Dostop
from treningi.models import Trening
from uporabniki.models import Uporabnik

from .models import DnevniCilj, Komentar, Vnos
from .views import kalorije, litri, napredek


def uporabnik(ime):
    return Uporabnik.objects.create_user(ime, f"{ime}@primer.si", "Geslo-12345", ime=ime.capitalize())


class OblikaNapredkaTest(SimpleTestCase):
    def test_litri_z_decimalno_vejico(self):
        self.assertEqual(litri(1500), "1,5 l")
        self.assertEqual(litri(2000), "2 l")
        self.assertEqual(litri(250), "0,25 l")

    def test_kalorije_brez_decimalk(self):
        self.assertEqual(kalorije(450.0), "450 kcal")
        self.assertEqual(kalorije(0), "0 kcal")

    def test_presezen_cilj_manjka_nic(self):
        self.assertEqual(napredek(3000, 2500, litri), "3 l od 2,5 l, manjka 0 l")
        self.assertEqual(napredek(1000, 2500, litri), "1 l od 2,5 l, manjka 1,5 l")


class NeveljavniVnosiTest(TestCase):
    def setUp(self):
        self.ana = uporabnik("ana")
        self.client.force_login(self.ana)

    def test_neveljaven_cilj_ne_zamenja_starega(self):
        self.client.post("/prehrana/cilj/", {"kcal": 2200, "voda_ml": 2500})
        for podatki in [{"kcal": 0, "voda_ml": 2500}, {"kcal": 2000, "voda_ml": -1}, {"kcal": 50000, "voda_ml": 2000}]:
            with self.subTest(podatki=podatki):
                self.assertRedirects(self.client.post("/prehrana/cilj/", podatki), "/prehrana/")
        cilj = DnevniCilj.objects.get()
        self.assertEqual((cilj.kcal, cilj.voda_ml, cilj.status), (2200, 2500, "AKTIVEN"))

    def test_teza_mora_biti_pozitivna(self):
        for teza in ["0", "-70", "abc"]:
            self.client.post("/casovnica/teza/", {"teza_kg": teza})
        self.assertFalse(Vnos.objects.exists())

    def test_predolg_opis_obroka_ni_shranjen(self):
        odgovor = self.client.post("/prehrana/", {"opis": "x" * 201, "kcal": 300})
        self.assertEqual(odgovor.status_code, 200)
        self.assertFalse(Vnos.objects.exists())

    def test_lastna_stran_sportnika_preusmeri_na_svojo(self):
        self.assertRedirects(self.client.get(f"/prehrana/{self.ana.pk}/"), "/prehrana/")
        self.assertRedirects(self.client.get(f"/casovnica/{self.ana.pk}/"), "/casovnica/")


class PrazenKomentarTest(TestCase):
    def test_prazen_komentar_ni_shranjen(self):
        ana, tomaz = uporabnik("ana"), uporabnik("tomaz")
        Dostop.objects.create(sportnik=ana, strokovnjak=tomaz, vrsta="TRENER", status="AKTIVEN")
        trening = Trening.objects.create(uporabnik=ana, trajanje_min=45, porabljene_kcal=300)
        self.client.force_login(tomaz)
        odgovor = self.client.post(f"/casovnica/{ana.pk}/komentar/", {"besedilo": "", "trening": trening.pk})
        self.assertEqual(odgovor.status_code, 404)
        self.assertFalse(Komentar.objects.exists())
