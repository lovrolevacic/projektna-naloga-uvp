
import pandas as pd
import requests
import os
from dotenv import load_dotenv
from io import StringIO

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def zajemi_filme_tmdb(n=100):
    '''Funkcija zajeme podatke iz strani TMDb'''
    if not API_KEY:
        raise ValueError("API ključ ni nastavljen. Preveri datoteko .env!")

    filmi = []
    page = 1

    while len(filmi) < n:
        url = f"{BASE_URL}/movie/top_rated?api_key={API_KEY}&language=en-US&page={page}"
        print(f"Pošiljam zahtevo na: {url}")  # DEBUG

        try:
            r = requests.get(url)
            r.raise_for_status()  # preveri HTTP status
        except requests.exceptions.RequestException as e:
            print(f"Napaka pri pošiljanju zahteve: {e}")
            break

        data = r.json()
        if "results" not in data:
            print(f"API odgovor ne vsebuje 'results': {data}")
            break

        for film in data["results"]:
            film_id = film["id"]
            # Pridobi podrobnosti o filmu
            det_url = f"{BASE_URL}/movie/{film_id}?api_key={API_KEY}&language=en-US"
            try:
                det_r = requests.get(det_url)
                det_r.raise_for_status()
                podrobnosti = det_r.json()
            except requests.exceptions.RequestException as e:
                print(f"Napaka pri pridobivanju podrobnosti filma {film_id}: {e}")
                continue

            release_date = podrobnosti.get("release_date", "")
            year = None
            if release_date and len(release_date) >= 4:
                try:
                    year = int(release_date[:4])
                except ValueError:
                    year = None

            filmi.append({
                "title": podrobnosti.get("title"),
                "year": year,
                "release_date": podrobnosti.get("release_date"),
                "vote_average": podrobnosti.get("vote_average"),
                "vote_count": podrobnosti.get("vote_count"),
                "revenue": podrobnosti.get("revenue"),
                "budget": podrobnosti.get("budget"),
                "runtime": podrobnosti.get("runtime")
            })
            if len(filmi) >= n:
                break
        page += 1

    return filmi

def zajemi_boxoffice():
    '''Finkcija zajeme podatke iz strani Box Office Mojo'''
    url = "https://www.boxofficemojo.com/chart/top_lifetime_gross/?area=XWW"
    r = requests.get(url)
    r.raise_for_status()

    tabele = pd.read_html(StringIO(r.text))
    df = tabele[0]  # Predpostavimo, da je prva tabela prava

    # Preimenujemo stolpce v ustrezne za združevanje
    df = df[['Title', 'Lifetime Gross', 'Year']]
    df = df.rename(columns={
        'Title': 'title',
        'Lifetime Gross': 'revenue',
        'Year': 'year'
    })

    # Očistimo revenue
    df['revenue'] = df['revenue'].replace('[\$,]', '', regex=True).astype(int)

    return df

