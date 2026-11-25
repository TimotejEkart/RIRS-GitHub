from django.test import TestCase

from uporabniki.models import Uporabnik
from vnosi.models import DnevniCilj, Vnos

ZASCITENE_STRANI = ["/", "/treningi/", "/statistika/misice/", "/prehrana/", "/casovnica/", "/dostop/", "/moji-sportniki/"]
SAMO_POST = ["/prehrana/voda/", "/prehrana/cilj/", "/casovnica/pocutje/", "/casovnica/teza/", "/odjava/"]


class DostopDoStraniTest(TestCase):
    def test_zascitene_strani_preusmerijo_na_prijavo(self):
        for url in ZASCITENE_STRANI:
            with self.subTest(url=url):
                self.assertRedirects(self.client.get(url), f"/prijava/?next={url}")

    def test_strani_za_vnos_ne_sprejmejo_get(self):
        ana = Uporabnik.objects.create_user("ana", "ana@primer.si", "Geslo-12345", ime="Ana")
        self.client.force_login(ana)
        for url in SAMO_POST:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 405)
        self.assertFalse(Vnos.objects.exists())
        self.assertFalse(DnevniCilj.objects.exists())
