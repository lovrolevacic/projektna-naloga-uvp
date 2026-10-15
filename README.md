# Ocene filmov in njihov finančni uspeh

Projektna naloga pri predmetu **Uvod v programiranje** (FMF UL).

Analiza povezuje ocene uporabnikov z Box Office podatki in odgovarja na
vprašanje, ali bolje ocenjeni filmi tudi več zaslužijo.

## Podatkovna vira

| Vir | Način zajema | Zajeti podatki |
|---|---|---|
| [TMDb](https://www.themoviedb.org/) | REST API (`requests`) | naslov, leto izida, povprečna ocena, število glasov, proračun, trajanje |
| [Box Office Mojo](https://www.boxofficemojo.com/) | zajem spletne tabele (`pandas.read_html`) | naslov, leto izida, skupni zaslužek |

Za vsak film, ki se pojavi v obeh virih, je izračunan še **ROI**
(donosnost investicije) kot `(zaslužek − proračun) / proračun`.

## Potek analize

1. **Zajem** (`zajem.py`) – strani TMDb se berejo zaporedno, za vsak film sledi
   še klic za podrobnosti. Zahteve so omejene s premorom, napake posamezne
   zahteve ne prekinejo zajema. API ključ se bere iz datoteke `.env`.
2. **Shranjevanje** (`shrani.py`) – oba vira se shranita v `data/` kot CSV.
3. **Poenotenje naslovov in združevanje** (`normalizacija.py`, `priprava.py`) –
   naslovi se pred združevanjem poenotijo (male črke, odstranitev diakritike
   in ločil, premik zadaj pripetega člena), da zapis oblike *Dark Knight, The*
   ustreza zapisu *The Dark Knight*. Na trenutnem naboru podatkov oba vira
   uporabljata isti zapis, zato poenotenje ne spremeni števila ujemanj; v kodi
   je zato, da združevanje ostane pravilno ob spremembi zapisa v katerem od
   virov. Združevanje poteka po poenotenem naslovu **in letu izida** — brez
   leta bi se izvirniki povezali z zaslužkom predelav (*The Lion King*
   1994/2019, *Beauty and the Beast* 1991/2017, *Aladdin* 1992/2019).
4. **Izračun ROI** (`izracun_roi.py`).
5. **Vizualizacija** (`graficni_prikaz.py`) – histogram ocen, ocena proti
   zaslužku, proračun proti zaslužku (dvojna logaritemska skala), ROI po letih,
   ocena proti ROI, dolžina filma proti zaslužku in oceni s Pearsonovim
   koeficientom, korelacijska matrika ter lestvici najvišjega zaslužka in
   najvišjega ROI.
6. **Analiza in ugotovitve** (`analiza.ipynb`).

## Struktura

```
main.py              zažene zajem obeh virov in shrani CSV
zajem.py             TMDb API in Box Office Mojo
shrani.py            shranjevanje v CSV
normalizacija.py     poenotenje naslovov za združevanje
priprava.py          branje, združevanje, izračun ROI
izracun_roi.py       izračun donosnosti
graficni_prikaz.py   grafi
analiza.ipynb        analiza in ugotovitve
test_projekt.py      testi
data/                zajeti podatki (CSV)
```

## Zagon

```bash
pip install -r requirements.txt
```

**Samo pregled analize:** odpri `analiza.ipynb`. Uporabijo se že shranjene
datoteke v `data/`, zajem ni potreben.

**Svež zajem podatkov:**

1. Ustvari `.env` po vzoru `.env.example` in vpiši svoj TMDb API ključ.
2. Zaženi zajem:

   ```bash
   python main.py            # 1000 filmov; že zajete podatke prebere iz data/
   python main.py --n 200    # manjši zajem
   python main.py --osvezi   # vsili ponoven zajem s TMDb
   ```

3. Ponovno zaženi `analiza.ipynb`.

Zajem 1000 filmov pošlje več kot tisoč zahtev in traja nekaj minut. Če
`data/filmi_tmdb.csv` že obstaja in vsebuje dovolj vrstic, se zajem preskoči.

## Testi

```bash
python -m pytest test_projekt.py
```

Testi pokrivajo poenotenje naslovov, izračun ROI in izbiro prave tabele na
strani Box Office Mojo. Omrežne povezave ne potrebujejo.

## Rezultat združevanja

Od 1000 najbolje ocenjenih filmov na TMDb in 200 najdonosnejših na Box Office
Mojo se jih v obeh virih pojavi **51**. Analiza temelji na tem preseku.

## Ugotovitve

Povezava med oceno in zaslužkom je šibka, povezava med proračunom in
zaslužkom pa občutno močnejša. Finančni uspeh je torej bolj odvisen od
vloženega denarja kot od sprejetja pri gledalcih.

Pri ROI je slika obrnjena: najvišjo donosnost dosegajo filmi z majhnim
proračunom, dragi in dobro ocenjeni filmi pa imajo pogosto skromen ROI.

**Omejitev:** oba vira sta lestvici najboljših, ne naključni vzorec. Filmi,
ki so propadli, v podatkih niso zajeti, zato ugotovitev ni mogoče posplošiti
na vse filme.

## Uporabljene knjižnice

`pandas`, `requests`, `python-dotenv`, `matplotlib`, `seaborn`, `lxml`
(za `read_html`) ter standardni moduli `os`, `re`, `io`, `time`, `argparse`
in `unicodedata`.
