def ortalama(*notlar):
    if not notlar:
        return 0
    return sum(notlar) / len(notlar)

def harf_notu(notlar):
    ort = ortalama(*notlar)
    if ort >= 90:
        return 'A'
    elif ort >= 80:
        return 'B'
    elif ort >= 70:
        return 'C'
    elif ort >= 60:
        return 'D'
    else:
        return 'F'

def durum_kontrol(notlar):
    harf = harf_notu(notlar)
    if harf in ['A', 'B', 'C', 'D']:
        return "Geçti"
    else:
        return "Kaldı"