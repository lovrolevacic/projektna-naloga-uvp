"""Graficni prikazi za analizo filmskih podatkov.

Vsaka funkcija sprejme pripravljen DataFrame in narise en graf.
Funkcije se zanesejo le na stolpce, ki jih same preverijo, zato jih je
mogoce poganjati tudi na delnih podatkih.
"""

import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")


def _zahtevaj(df, *stolpci):
    """Vrni True, ce so vsi navedeni stolpci prisotni; sicer izpisi opozorilo."""
    manjkajoci = [s for s in stolpci if s not in df.columns]
    if manjkajoci:
        print(f"Manjkajo stolpci: {', '.join(manjkajoci)}. Graf je preskocen.")
        return False
    return True


def graf_0_histogram_ocen(df):
    """Porazdelitev povprecnih ocen TMDb."""
    if not _zahtevaj(df, "vote_average"):
        return
    plt.figure(figsize=(9, 5))
    sns.histplot(df["vote_average"].dropna(), bins=20, kde=True)
    plt.title("Porazdelitev ocen (TMDb)")
    plt.xlabel("Povprecna ocena")
    plt.ylabel("Stevilo filmov")
    plt.tight_layout()
    plt.show()


def graf_1_vote_vs_revenue(df):
    """Ocena v odvisnosti od zasluzka (logaritemska os y)."""
    if not _zahtevaj(df, "vote_average", "revenue_bo"):
        return
    podatki = df[df["revenue_bo"] > 0]
    plt.figure(figsize=(9, 5))
    sns.scatterplot(data=podatki, x="vote_average", y="revenue_bo")
    plt.yscale("log")
    plt.title("Ocena in zasluzek")
    plt.xlabel("Ocena (vote_average)")
    plt.ylabel("Zasluzek v USD (log)")
    plt.tight_layout()
    plt.show()


def graf_2_budget_vs_revenue(df):
    """Proracun v odvisnosti od zasluzka na dvojni logaritemski skali."""
    if not _zahtevaj(df, "budget", "revenue_bo"):
        return
    podatki = df[(df["budget"] > 0) & (df["revenue_bo"] > 0)]
    plt.figure(figsize=(9, 6))
    plt.scatter(podatki["budget"], podatki["revenue_bo"],
                alpha=0.7, edgecolors="k", linewidths=0.5)
    plt.xscale("log")
    plt.yscale("log")
    plt.title("Proracun in zasluzek")
    plt.xlabel("Proracun v USD (log)")
    plt.ylabel("Zasluzek v USD (log)")
    plt.tight_layout()
    plt.show()


def graf_3_roi_po_letu(df, od_leta=2000):
    """Porazdelitev ROI po letih izida."""
    if not _zahtevaj(df, "year", "roi"):
        return
    podatki = df[(df["year"] >= od_leta) & df["roi"].notna()]
    if podatki.empty:
        print("Za izbrano obdobje ni podatkov o ROI.")
        return
    plt.figure(figsize=(13, 6))
    sns.boxplot(data=podatki, x="year", y="roi", showfliers=False)
    plt.xticks(rotation=45)
    plt.title(f"ROI po letu izida (od {od_leta})")
    plt.xlabel("Leto")
    plt.ylabel("ROI")
    plt.tight_layout()
    plt.show()


def graf_4_ocena_vs_roi(df):
    """Ocena v odvisnosti od ROI."""
    if not _zahtevaj(df, "vote_average", "roi"):
        return
    podatki = df[df["roi"].notna()]
    plt.figure(figsize=(9, 6))
    plt.scatter(podatki["vote_average"], podatki["roi"],
                alpha=0.6, color="green", edgecolors="k", linewidths=0.5)
    plt.title("Ocena in ROI")
    plt.xlabel("Ocena (TMDb)")
    plt.ylabel("ROI")
    plt.tight_layout()
    plt.show()


def graf_5_6_analiza_trajanja(df):
    """Povezava dolzine filma z zasluzkom in z oceno; izpise korelaciji."""
    if not _zahtevaj(df, "runtime"):
        return

    for stolpec, naslov, oznaka in (
        ("revenue_bo", "Dolzina filma in zasluzek", "Zasluzek v USD"),
        ("vote_average", "Dolzina filma in ocena", "Povprecna ocena"),
    ):
        if stolpec not in df.columns:
            continue
        podatki = df[["runtime", stolpec]].dropna()
        if podatki.empty:
            continue
        r = podatki["runtime"].corr(podatki[stolpec])
        plt.figure(figsize=(9, 5))
        sns.scatterplot(data=podatki, x="runtime", y=stolpec)
        plt.title(f"{naslov} (Pearsonov r = {r:.2f})")
        plt.xlabel("Dolzina filma v minutah")
        plt.ylabel(oznaka)
        plt.tight_layout()
        plt.show()
        print(f"{naslov}: Pearsonov r = {r:.3f} (n = {len(podatki)})")


def graf_7_korelacijska_matrika(df):
    """Korelacije med stevilskimi spremenljivkami."""
    stevilski = df.select_dtypes("number").drop(columns=["year"], errors="ignore")
    if stevilski.shape[1] < 2:
        print("Premalo stevilskih stolpcev za korelacijsko matriko.")
        return
    plt.figure(figsize=(9, 7))
    sns.heatmap(stevilski.corr(), annot=True, fmt=".2f", cmap="viridis",
                square=True, cbar_kws={"shrink": 0.8})
    plt.title("Korelacije med stevilskimi spremenljivkami")
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()


def graf_8_top10_roi(df, n=10):
    """Vodoravni stolpicni prikaz n filmov z najvisjim ROI."""
    if not _zahtevaj(df, "title", "roi"):
        return
    najboljsi = df.dropna(subset=["roi"]).nlargest(n, "roi")
    if najboljsi.empty:
        print("Ni podatkov o ROI.")
        return
    plt.figure(figsize=(9, 5))
    sns.barplot(data=najboljsi, y="title", x="roi", orient="h")
    plt.title(f"Najvisji ROI: {len(najboljsi)} filmov")
    plt.xlabel("ROI")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()


def graf_9_top10_zasluzek(df, n=10):
    """Vodoravni stolpicni prikaz n filmov z najvisjim zasluzkom."""
    if not _zahtevaj(df, "title", "revenue_bo"):
        return
    najboljsi = df.nlargest(n, "revenue_bo")
    plt.figure(figsize=(9, 5))
    sns.barplot(data=najboljsi, y="title", x="revenue_bo", orient="h")
    plt.title(f"Najvisji zasluzek: {len(najboljsi)} filmov")
    plt.xlabel("Zasluzek v USD")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()
