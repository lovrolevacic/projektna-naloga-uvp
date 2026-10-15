"""Testi za projektno nalogo. Omrezne povezave niso potrebne."""

from io import StringIO
from math import isnan

import pandas as pd
import pytest

from izracun_roi import izracunaj_roi
from normalizacija import normaliziraj_naslov
from zajem import _izberi_tabelo, _leto_iz_datuma


class TestNormalizacija:
    @pytest.mark.parametrize("vhod, pricakovano", [
        ("The Dark Knight", "dark knight"),
        ("Dark Knight, The", "dark knight"),
        ("WALL-E", "wall e"),
        ("Amélie", "amelie"),
        ("  Up  ", "up"),
        ("A Beautiful Mind", "beautiful mind"),
    ])
    def test_poenoti(self, vhod, pricakovano):
        assert normaliziraj_naslov(vhod) == pricakovano

    def test_razlicna_zapisa_dasta_isti_kljuc(self):
        assert normaliziraj_naslov("The Lion King") == normaliziraj_naslov("Lion King, The")

    def test_none(self):
        assert normaliziraj_naslov(None) is None


class TestRoi:
    def test_izracun(self):
        assert izracunaj_roi(100, 250) == 1.5

    def test_izguba(self):
        assert izracunaj_roi(200, 100) == -0.5

    @pytest.mark.parametrize("budget, revenue", [(0, 250), (None, 250), (100, None), ("x", 1)])
    def test_manjkajoci_podatki_dajo_nan(self, budget, revenue):
        assert isnan(izracunaj_roi(budget, revenue))


class TestZajem:
    def test_leto_iz_datuma(self):
        assert _leto_iz_datuma("2008-07-16") == 2008
        assert _leto_iz_datuma("") is None
        assert _leto_iz_datuma(None) is None

    def test_izbere_pravo_tabelo(self):
        html = """
        <table><tr><th>Foo</th></tr><tr><td>1</td></tr></table>
        <table><tr><th>Rank</th><th>Title</th><th>Lifetime Gross</th><th>Year</th></tr>
        <tr><td>1</td><td>Avatar</td><td>$2,923,706,026</td><td>2009</td></tr></table>
        """
        tabela = _izberi_tabelo(pd.read_html(StringIO(html)))
        assert "Lifetime Gross" in tabela.columns

    def test_javi_napako_brez_prave_tabele(self):
        html = "<table><tr><th>A</th></tr><tr><td>1</td></tr></table>"
        with pytest.raises(ValueError):
            _izberi_tabelo(pd.read_html(StringIO(html)))
