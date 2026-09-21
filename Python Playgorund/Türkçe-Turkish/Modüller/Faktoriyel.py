def hesapla(n):
    if n < 0:
        return "Negatif sayının faktöriyeli hesaplanamaz."
    elif n == 0 or n == 1:
        return 1
    else:
        faktoriyel = 1
        for i in range(2, n + 1):
            faktoriyel *= i
        return faktoriyel

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True