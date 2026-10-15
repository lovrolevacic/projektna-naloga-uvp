"""Pomozne funkcije za poenotenje naslovov filmov pred zdruzevanjem virov."""

import re
import unicodedata

# Cleni, ki jih razlicni viri zapisujejo razlicno ("The Dark Knight" / "Dark Knight, The").
CLENI = ("the ", "a ", "an ")


def normaliziraj_naslov(naslov):
    """Vrni poenoteno obliko naslova, primerno za ujemanje med viri.

    Postopek: male crke, odstranitev diakritike, premik zadaj pripetega clena
    na zacetek, odstranitev locil in odvecnih presledkov ter odstranitev
    zacetnega clena.

    >>> normaliziraj_naslov("The Dark Knight")
    'dark knight'
    >>> normaliziraj_naslov("Dark Knight, The")
    'dark knight'
    >>> normaliziraj_naslov("WALL-E")
    'wall e'
    >>> normaliziraj_naslov(None) is None
    True
    """
    if naslov is None:
        return None
    if not isinstance(naslov, str):
        naslov = str(naslov)

    besedilo = unicodedata.normalize("NFKD", naslov)
    besedilo = "".join(z for z in besedilo if not unicodedata.combining(z))
    besedilo = besedilo.lower().strip()

    # "Dark Knight, The" -> "the dark knight"
    ujemanje = re.match(r"^(.*),\s*(the|a|an)$", besedilo)
    if ujemanje:
        besedilo = f"{ujemanje.group(2)} {ujemanje.group(1)}"

    besedilo = re.sub(r"[^a-z0-9]+", " ", besedilo).strip()

    for clen in CLENI:
        if besedilo.startswith(clen):
            besedilo = besedilo[len(clen):]
            break

    return re.sub(r"\s+", " ", besedilo).strip()


def dodaj_kljuc(df, stolpec_naslova="title"):
    """Dodaj stolpec 'kljuc' s poenotenim naslovom. Vrne nov DataFrame."""
    df = df.copy()
    df["kljuc"] = df[stolpec_naslova].map(normaliziraj_naslov)
    return df
