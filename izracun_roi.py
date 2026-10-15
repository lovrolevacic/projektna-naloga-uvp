"""Izracun donosnosti investicije (ROI) za posamezen film."""

from math import nan


def izracunaj_roi(budget, revenue):
    """Vrni ROI = (zasluzek - proracun) / proracun.

    Vrne nan, kadar proracuna ali zasluzka ni oziroma je proracun nicelen,
    da ostane stolpec stevilski in se vrstice ne izgubijo.

    >>> izracunaj_roi(100, 250)
    1.5
    >>> izracunaj_roi(0, 250)
    nan
    >>> izracunaj_roi(None, 250)
    nan
    >>> izracunaj_roi(100, None)
    nan
    """
    try:
        budget = float(budget)
        revenue = float(revenue)
    except (TypeError, ValueError):
        return nan

    if budget <= 0 or revenue != revenue or budget != budget:
        return nan

    return (revenue - budget) / budget
