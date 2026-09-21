import Matematik as mat
import hesaplama

print(f"16'nın karekökü: {mat.karekok(16)}")
print("-" * 30)


sayi = 5
print(f"{sayi}! = {hesaplama.faktoriyel(sayi)}")

print("=" * 30)


test_sayilari = [1, 7, 12, 29]
for s in test_sayilari:
    durum = "Asaldır" if hesaplama.is_prime(s) else "Asal Değildir"
    print(f"{s} sayısı: {durum}")