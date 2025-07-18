# Analiza filmskih podatkov (TMDb in Box Office Mojo)

Za projektno nalogo pri predmetu Uvod v programiranje sem izbral analizo filmskih podatkov iz dveh virov:
- TMDb (The Movie Database) – podatki o filmih z ocenami uporabnikov,
- Box Office Mojo – podatki o zaslužku filmov v kinematografih.

Cilj projekta je povezati ocene filmov s finančnimi metrikami (proračun, zaslužek, donosnost) in analizirati, kateri dejavniki vplivajo na uspešnost filmov.

Za vsak film so bili zbrani naslednji podatki:

Iz TMDb:
- naslov filma,
- leto izida,
- povprečna ocena uporabnikov,
- število glasov,
- proračun,
- trajanje filma.

Iz Box Office Mojo:
- naslov filma,
- leto izida,
- zaslužek.

Dodatno je bil za vsak film izračunan še ROI (donosnost investicije).

## Analiza vključuje

- čiščenje in povezovanje podatkov iz obeh virov,
- standardizacijo naslovov za uspešno ujemanje,
- izračun ROI,
- vizualizacijo rezultatov:
  - histogram ocen (TMDb),
  - razmerje med proračunom in zaslužkom,
  - top 10 filmov po zaslužku,
  - top 10 filmov po ROI,
  - korelacijska matrika številčnih spremenljivk.

## Navodila za uporabo

Če želiš samo pregledati analizo, odpri datoteko `analiza.ipynb` v okolju Jupyter Notebook. V tem primeru se uporabijo že shranjene `.csv` datoteke v mapi `data/`.

Če želiš sam zajeti sveže podatke:

1. Zaženi datoteko `main.py`. Ta bo:
   - zajela podatke iz TMDb in Box Office Mojo,
   - jih shranila v `.csv` datoteke v mapi `data/`.

2. Nato odpri `analiza.ipynb` in ponovno zaženi celoten zvezek.

Uporabljene knjižnice so requests, pandas, matplotlib, seaborn, os, re, io in plotly.express za zemljevid na koncu analize
