import os
import pandas as pd

def shrani_csv(podatki, ime):
    # Preveri, če mapa obstaja, če ne, jo ustvari
    parent_dir = os.path.dirname(ime)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    df = pd.DataFrame(podatki)
    df.to_csv(ime, index=False)