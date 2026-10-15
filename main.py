"""Zazeni zajem podatkov iz obeh virov in jih shrani v mapo data/.

Uporaba:
    python main.py              # zajem 1000 filmov (predpomnilnik se uposteva)
    python main.py --n 200      # zajem 200 filmov
    python main.py --osvezi     # vsili ponovni zajem s TMDb
"""

import argparse

import zajem
from shrani import shrani_csv


def main():
    razclenjevalnik = argparse.ArgumentParser(description=__doc__)
    razclenjevalnik.add_argument("--n", type=int, default=1000,
                                 help="stevilo filmov, zajetih s TMDb")
    razclenjevalnik.add_argument("--osvezi", action="store_true",
                                 help="prezri predpomnjene podatke in zajemi znova")
    argumenti = razclenjevalnik.parse_args()

    filmi = zajem.zajemi_filme_tmdb(argumenti.n, osvezi=argumenti.osvezi)
    shrani_csv(filmi, "data/filmi_tmdb.csv")

    box_office = zajem.zajemi_boxoffice()
    shrani_csv(box_office, "data/bo_mojo.csv")


if __name__ == "__main__":
    main()
