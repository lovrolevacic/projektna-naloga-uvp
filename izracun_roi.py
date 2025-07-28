def izracunaj_roi(budget, revenue):
    """Izračunaj ROI – Return on Investment."""
    if budget and budget > 0:
        return ((revenue - budget) / budget) * 100 # Množenje s 100, da dobimo rezultat v procentih
    return None
