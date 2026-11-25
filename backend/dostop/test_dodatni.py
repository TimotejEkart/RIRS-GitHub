from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Dostop


def uporabnik(ime):
    return Uporabnik.objects.create_user(ime, f"{ime}@primer.si", "Geslo-12345", ime=ime.capitalize())


class PreklicInOdgovorTest(TestCase):
    def setUp(self):
        self.ana, self.marko, self.tomaz = uporabnik("ana"), uporabnik("marko"), uporabnik("tomaz")
        self.dostop = Dostop.objects.create(sportnik=self.ana, strokovnjak=self.tomaz, vrsta="TRENER", status="AKTIVEN")

    def test_tujega_dostopa_ni_mogoce_preklicati(self):
        # marko ni športnik tega dostopa, tomaz pa je samo strokovnjak
        for kdo in [self.marko, self.tomaz]:
            self.client.force_login(kdo)
            self.assertEqual(self.client.post(f"/dostop/{self.dostop.pk}/preklici/").status_code, 404)
        self.dostop.refresh_from_db()
        self.assertEqual(self.dostop.status, "AKTIVEN")

    def test_preklicanega_povabila_ni_mogoce_sprejeti(self):
        self.dostop.status = "PREKLICAN"
        self.dostop.save()
        self.client.force_login(self.tomaz)
        self.assertEqual(self.client.post(f"/moji-sportniki/povabilo/{self.dostop.pk}/sprejmi/").status_code, 404)
        self.dostop.refresh_from_db()
        self.assertEqual(self.dostop.status, "PREKLICAN")

    def test_ze_preklicanega_dostopa_ni_mogoce_znova_preklicati(self):
        self.client.force_login(self.ana)
        self.assertRedirects(self.client.post(f"/dostop/{self.dostop.pk}/preklici/"), "/dostop/")
        self.assertEqual(self.client.post(f"/dostop/{self.dostop.pk}/preklici/").status_code, 404)

    def test_opis_dostopa(self):
        self.assertEqual(str(self.dostop), "tomaz → ana (trener)")
