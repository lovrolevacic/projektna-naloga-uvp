
import zajem
from shrani import shrani_csv

def main():
    filmi_tmdb = zajem.zajemi_filme_tmdb(1000) #1000 najbolje ocenjenih filmov
    shrani_csv(filmi_tmdb, "data/filmi_tmdb.csv")

    df_bo = zajem.zajemi_boxoffice()
    shrani_csv(df_bo, "data/bo_mojo.csv")

if __name__ == "__main__":
    main()

