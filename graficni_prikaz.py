import matplotlib.pyplot as plt
import seaborn as sns

def graf_1_vote_vs_revenue(df):
    """
    Prikaže raztreseni graf, ki prikazuje povezavo med povprečno oceno filma in njegovim zaslužkom.
    Dobiček je prikazan v logaritemski skali, da lažje vidimo razlike med filmi z zelo različnimi prihodki.
    """    
    plt.figure(figsize=(8, 5))
    sns.scatterplot(data=df, x="vote_average", y="revenue_bo")
    plt.yscale("log")
    plt.title("Ocena vs Dobiček (Box Office)")
    plt.xlabel("Ocena (vote_average)")
    plt.ylabel("Dobiček (revenue_bo, log)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graf_2_budget_vs_revenue(df):
    """
    Prikaže raztreseni graf povezave med proračunom in zaslužkom filmov.
    Uporablja logaritemsko skalo na obeh oseh, da poudari razlike med filmi z različnimi velikostmi proračuna.
    """    
    df_filtered = df[(df["budget"] > 0) & (df["revenue_bo"] > 0)]
    plt.figure(figsize=(10, 6))
    plt.scatter(df_filtered["budget"], df_filtered["revenue_bo"],
                alpha=0.7, edgecolors="k", linewidths=0.5)
    plt.title("Proračun vs. Zaslužek filmov")
    plt.xlabel("Proračun ($, log)")
    plt.ylabel("Zaslužek ($, log)")
    plt.xscale("log")
    plt.yscale("log")
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def graf_3_roi_po_letu(df):
    """
    Prikaže boxplot ROI (donosnosti investicije) filmov po letih od 2000 naprej.
    Omogoča primerjavo, kako uspešni so bili filmi glede na proračun v različnih letih.
    """    
    plt.figure(figsize=(14, 6))
    sns.boxplot(x="year", y="roi", data=df[df["year"] >= 2000], showfliers=False)
    plt.xticks(rotation=45)
    plt.title("ROI filmov po letu (od 2000 naprej)")
    plt.xlabel("Leto")
    plt.ylabel("ROI")
    plt.grid(True, axis="y", linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def graf_4_ocena_vs_roi(df):
    """
    Prikaže raztreseni graf med oceno filma (vote_average) in ROI.
    Namen je ugotoviti, ali obstaja povezava med kakovostjo filma in njegovim finančnim uspehom.
    """    
    plt.figure(figsize=(10, 6))
    plt.scatter(df["vote_average"], df["roi"],
                alpha=0.6, color="green", edgecolors="k", linewidths=0.5)
    plt.title("Ocena vs. ROI")
    plt.xlabel("Ocena (TMDb)")
    plt.ylabel("ROI")
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.show()


def graf_5_6_analiza_trajanja(df):
    """
    Prikaže dve analizi:
    - povezavo med dolžino filma (runtime) in zaslužkom,
    - povezavo med dolžino filma in povprečno oceno.

    S tem preverjamo, ali daljši filmi dosegajo večji uspeh pri gledalcih in na blagajni.
    """    
    # Prvi graf: trajanje filma vs. zaslužek
    if "revenue" in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="runtime", y="revenue")
        plt.title("Povezava med dolžino filma in zaslužkom")
        plt.xlabel("Dolžina filma (v minutah)")
        plt.ylabel("Zaslužek (USD)")
        plt.tight_layout()
        plt.show()

    # Drugi graf: trajanje filma vs. ocena
    if "vote_average" in df.columns:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x="runtime", y="vote_average")
        plt.title("Povezava med dolžino filma in oceno")
        plt.xlabel("Dolžina filma (v minutah)")
        plt.ylabel("Povprečna ocena")
        plt.tight_layout()
        plt.show()


def graf_7_korelacijska_matrika(df):
    """
    Izriše korelacijsko matriko med vsemi številskimi spremenljivkami v podatkovnem okviru.
    Pomaga pri iskanju medsebojnih povezav med podatki, kot so proračun, ocena, zaslužek...
    """    
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df.corr(numeric_only=True),
        annot=True,
        fmt=".2f",
        cmap="viridis",
        square=True,
        cbar_kws={"shrink": 0.8}
    )
    plt.title("Korelacije med številskimi spremenljivkami", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.show()




