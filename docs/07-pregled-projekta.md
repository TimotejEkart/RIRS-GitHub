# Pregled projekta

Pregledal sem dokumentacijo v `docs/`, arhitekturne odločitve (ADR 0001–0009) in kodo. Aplikacijo sem zagnal lokalno po navodilih v README, le PostgreSQL sem namesto lokalne namestitve zagnal v Dockerju. Migracije in začetni podatki so se naložili brez težav, vseh 90 obstoječih testov je uspešnih.

## Implementirane funkcionalnosti MVP

| # | Funkcionalnost | Stanje |
|---|----------------|--------|
| 1 | Registracija in prijava | implementirano |
| 2 | Hitro beleženje treninga | implementirano |
| 3 | Zemljevid obremenitve mišic | implementirano |
| 4 | Voda in obroki z dnevnim ciljem | implementirano |
| 5 | Dostop za trenerja in prehranskega svetovalca | implementirano |
| 6 | Plan treningov z različicami | ni implementirano |
| 7 | Časovnica in počutje | implementirano |

Implementiranih je 6 od 7 funkcionalnosti MVP. Plana treningov (US-06) v projektu ni, ni modelov, strani ne poti.
## Pregled uporabniških zgodb

Pregledal sem uporabniške zgodbe US-01 do US-05. Vsak pogoj sprejemljivosti sem preizkusil v brskalniku s testnimi uporabniki (športnik, trener, prehranska svetovalka).

### US-01 – Registracija in prijava

- Registracija zahteva ime, uporabniško ime, e-pošto in geslo. ✔
- Pri zasedenem uporabniškem imenu ali e-pošti se račun ne ustvari, napaka je izpisana pri pravem polju. ✔
- Prijava deluje z uporabniškim imenom in z e-pošto. ✔
- Ob napačnem geslu se izpiše »Napačni podatki za prijavo«. ✔
- Uporabnik, ki mu je administrator v adminu odkljukal »Active«, se ne more prijaviti. ✔

Po registraciji uporabnik ni samodejno prijavljen, ampak ga aplikacija preusmeri na prijavo. Zgodba tega ne zahteva.

### US-02 – Beleženje treninga

- Vaja se izbere s seznama, za vsako serijo se vpišejo ponovitve in teža. ✔
- K treningu se vpišeta trajanje in porabljene kalorije. ✔
- Gumb »Kopiraj trening« odpre nov trening z istimi vajami in serijami, številke je mogoče popraviti. ✔
- Shranjen trening se prikaže na seznamu preteklih treningov in na časovnici. ✔
- Športnik vaj ne more dodajati ali urejati, to lahko samo administrator. ✔

### US-03 – Zemljevid obremenitve mišic

- Zemljevid prikaže telo spredaj in zadaj, mišice so obarvane na lestvici 0–10. ✔
- Izračun ustreza pravilu: pri 4 serijah potiska s prsi in 2 serijah iztegovanja komolcev dobijo prsa 10, triceps 10 in ramena 5. ✔
- Netrenirane mišice so sive. ✔
- Privzeto obdobje je 7 dni, izbrati je mogoče 30 dni ali poljuben razpon. ✔
- Brez treningov v obdobju so vse mišice sive in izpiše se »V tem obdobju ni zabeleženih treningov«. ✔

### US-04 – Voda in obroki z dnevnim ciljem

- Gumb »+250 ml« doda 250 ml vode. ✔
- Obrok se vnese z opisom in kalorijami. ✔
- Dnevni cilj si športnik nastavi sam, velja od dneva nastavitve. ✔
- Za danes se izpiše npr. »1,5 l od 2,5 l, manjka 1 l«. ✔
- Pretekli dan se primerja s ciljem, ki je veljal tisti dan (preizkušeno s ciljem 2 l iz prejšnjega tedna in današnjim ciljem 2,5 l). ✔

### US-05 – Dostop za trenerja in prehranskega svetovalca

- Povabilo se pošlje z uporabniškim imenom in vrsto dostopa, za neobstoječe ime se izpiše »Uporabnik s tem uporabniškim imenom ne obstaja.«. ✔
- Pred sprejemom povabljeni ne vidi nobenih podatkov (strani športnika vrnejo 404). ✔
- Po sprejemu je športnik na seznamu »Moji športniki«. ✔
- Trener vidi treninge in zemljevid mišic, ne pa vode in obrokov. Prehranska svetovalka vidi vodo, obroke in kalorije treningov, ne pa vaj in zemljevida. ✔
- Po preklicu povabljeni ne vidi več podatkov in športnika ni več na njegovem seznamu. ✔

