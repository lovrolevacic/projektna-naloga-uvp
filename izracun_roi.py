def izracunaj_roi(budget, revenue):
    """Izračunaj ROI – Return on Investment."""
    if budget and budget > 0:
        return (revenue - budget) / budget
    return None
