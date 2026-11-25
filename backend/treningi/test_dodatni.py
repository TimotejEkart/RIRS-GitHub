from django.test import TestCase

from uporabniki.models import Uporabnik

from .models import Serija, Trening, Vaja, VajaMisica


class OpisiModelovTest(TestCase):
    fixtures = ["zacetni_podatki"]

    def test_opis_serije_in_misice_vaje(self):
        ana = Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        trening = Trening.objects.create(uporabnik=ana, trajanje_min=60, porabljene_kcal=400)
        pocep = Vaja.objects.get(ime="Počep")
        serija = Serija.objects.create(trening=trening, vaja=pocep, zaporedna_st=1, ponovitve=8, teza_kg=82.5)
        self.assertEqual(str(serija), "Počep: 8 × 82.5 kg")
        glavna = VajaMisica.objects.filter(vaja=pocep, tip="GLAVNA").first()
        self.assertTrue(str(glavna).startswith("Počep – "))
        self.assertTrue(str(glavna).endswith(f"({glavna.get_tip_display()})"))

    def test_kopija_neobstojecega_treninga_404(self):
        ana = Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        self.client.force_login(ana)
        self.assertEqual(self.client.get("/treningi/kopiraj/99999/").status_code, 404)
