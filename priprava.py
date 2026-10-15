"""Branje shranjenih virov, zdruzevanje in izracun izpeljanih stolpcev."""

import pandas as pd

from izracun_roi import izracunaj_roi
from normalizacija import dodaj_kljuc


def nalozi(pot_tmdb="data/filmi_tmdb.csv", pot_bo="data/bo_mojo.csv"):
    """Vrni (tmdb, bo) kot DataFrame-a."""
    return pd.read_csv(pot_tmdb), pd.read_csv(pot_bo)


def zdruzi(tmdb, bo, porocaj=True):
    """Zdruzi vira po poenotenem naslovu in letu ter dodaj stolpec roi.

    Zdruzevanje po surovem naslovu zavrze filme, ki jih vira zapisujeta
    razlicno, zato naslov najprej poenotimo (glej normalizacija.py).
    """
    tmdb_k = dodaj_kljuc(tmdb)
    bo_k = dodaj_kljuc(bo)

    df = pd.merge(tmdb_k, bo_k, on=["kljuc", "year"], suffixes=("_tmdb", "_bo"))
    df = df.drop(columns=["revenue_tmdb", "title_bo"], errors="ignore")
    df = df.rename(columns={"title_tmdb": "title"})
    df["roi"] = [izracunaj_roi(b, r) for b, r in zip(df["budget"], df["revenue_bo"])]

    if porocaj:
        surovo = pd.merge(tmdb, bo, on=["title", "year"])
        print(f"Zdruzenih filmov po poenotenem naslovu: {len(df)}")
        print(f"Za primerjavo, zdruzevanje po surovem naslovu da: {len(surovo)}")
        print(f"Filmov z izracunanim ROI: {int(df['roi'].notna().sum())}")

    return df.drop(columns=["kljuc"])
