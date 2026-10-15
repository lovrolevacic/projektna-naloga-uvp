"""Zajem podatkov o filmih iz TMDb (REST API) in Box Office Mojo (spletna tabela)."""

import os
import time
from io import StringIO

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

PREMOR = 0.25          # sekunde med zaporednimi zahtevami na TMDb
CASOVNA_OMEJITEV = 15  # sekunde do prekinitve posamezne zahteve
BO_URL = "https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW"
GLAVA = {"User-Agent": "projektna-naloga-uvp/1.0"}

STOLPCI_TMDB = ["title", "year", "release_date", "vote_average",
                "vote_count", "revenue", "budget", "runtime"]


def _leto_iz_datuma(datum):
    """Vrni leto iz niza oblike 'YYYY-MM-DD' ali None."""
    if isinstance(datum, str) and len(datum) >= 4 and datum[:4].isdigit():
        return int(datum[:4])
    return None


def zajemi_filme_tmdb(n=100, predpomnilnik="data/filmi_tmdb.csv", osvezi=False):
    """Zajemi n najbolje ocenjenih filmov s TMDb in vrni DataFrame.

    Ce predpomnjena datoteka ze obstaja in ima dovolj vrstic, je zajem
    preskocen (osvezi=True ga vsili). Tako ponovni zagon ne obremeni API-ja
    z vec kot tisoc zahtevami.
    """
    if not osvezi and predpomnilnik and os.path.exists(predpomnilnik):
        df = pd.read_csv(predpomnilnik)
        if len(df) >= n:
            print(f"Uporabljam predpomnjene podatke: {predpomnilnik} ({len(df)} filmov).")
            return df.head(n)

    if not API_KEY:
        raise ValueError(
            "API kljuc ni nastavljen. Ustvari datoteko .env po vzoru .env.example "
            "in vanjo vpisi TMDB_API_KEY."
        )

    filmi = []
    stran = 1
    with requests.Session() as seja:
        seja.headers.update(GLAVA)

        while len(filmi) < n:
            try:
                odgovor = seja.get(
                    f"{BASE_URL}/movie/top_rated",
                    params={"api_key": API_KEY, "language": "en-US", "page": stran},
                    timeout=CASOVNA_OMEJITEV,
                )
                odgovor.raise_for_status()
            except requests.exceptions.RequestException as napaka:
                print(f"Napaka pri branju strani {stran}: {napaka}")
                break

            rezultati = odgovor.json().get("results", [])
            if not rezultati:
                print(f"Stran {stran} ne vsebuje rezultatov; zajem koncan.")
                break

            for film in rezultati:
                podrobnosti = _zajemi_podrobnosti(seja, film["id"])
                if podrobnosti is None:
                    continue
                filmi.append(podrobnosti)
                if len(filmi) >= n:
                    break
                time.sleep(PREMOR)

            print(f"Zajetih {len(filmi)} / {n} filmov.")
            stran += 1

    return pd.DataFrame(filmi, columns=STOLPCI_TMDB)


def _zajemi_podrobnosti(seja, film_id):
    """Vrni slovar s podrobnostmi enega filma ali None ob napaki."""
    try:
        odgovor = seja.get(
            f"{BASE_URL}/movie/{film_id}",
            params={"api_key": API_KEY, "language": "en-US"},
            timeout=CASOVNA_OMEJITEV,
        )
        odgovor.raise_for_status()
    except requests.exceptions.RequestException as napaka:
        print(f"Napaka pri filmu {film_id}: {napaka}")
        return None

    p = odgovor.json()
    return {
        "title": p.get("title"),
        "year": _leto_iz_datuma(p.get("release_date")),
        "release_date": p.get("release_date"),
        "vote_average": p.get("vote_average"),
        "vote_count": p.get("vote_count"),
        "revenue": p.get("revenue"),
        "budget": p.get("budget"),
        "runtime": p.get("runtime"),
    }


def _izberi_tabelo(tabele):
    """Vrni prvo tabelo, ki vsebuje pricakovane stolpce.

    Zanasanje na tabele[0] je krhko: ce stran doda tabelo pred lestvico,
    se zajem tiho pokvari.
    """
    potrebni = {"Title", "Lifetime Gross", "Year"}
    for tabela in tabele:
        if potrebni.issubset(set(tabela.columns)):
            return tabela
    raise ValueError(
        "Na strani ni tabele s stolpci Title, Lifetime Gross in Year. "
        "Struktura strani se je verjetno spremenila."
    )


def zajemi_boxoffice():
    """Zajemi lestvico najdonosnejsih filmov z Box Office Mojo in vrni DataFrame."""
    odgovor = requests.get(BO_URL, headers=GLAVA, timeout=CASOVNA_OMEJITEV)
    odgovor.raise_for_status()

    tabela = _izberi_tabelo(pd.read_html(StringIO(odgovor.text)))
    df = tabela[["Title", "Lifetime Gross", "Year"]].rename(
        columns={"Title": "title", "Lifetime Gross": "revenue", "Year": "year"}
    )

    df["revenue"] = (
        df["revenue"].astype(str).str.replace(r"[^0-9]", "", regex=True)
    )
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    return df.dropna(subset=["revenue"]).reset_index(drop=True)
