"""Shranjevanje zajetih podatkov v CSV."""

import os

import pandas as pd


def shrani_csv(podatki, ime):
    """Shrani podatke (DataFrame ali seznam slovarjev) v CSV; ustvari mapo, ce manjka."""
    mapa = os.path.dirname(ime)
    if mapa:
        os.makedirs(mapa, exist_ok=True)

    df = podatki if isinstance(podatki, pd.DataFrame) else pd.DataFrame(podatki)
    df.to_csv(ime, index=False)
    print(f"Shranjeno: {ime} ({len(df)} vrstic)")
    return df
