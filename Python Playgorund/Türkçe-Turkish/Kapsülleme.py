class bankahesabı():
    def __init__(self, ad, soyad, hesap_no, bakiye):
        self.ad = ad
        self.soyad = soyad
        self.hesap_no = hesap_no
        self.__bakiye = bakiye

    def bakiye_goster(self):
        print(f"{self.ad} {self.soyad} hesabının bakiyesi: {self.__bakiye} TL")

    def para_yatır(self, miktar):
        if miktar > 0:
            self.__bakiye += miktar
            print(f"{miktar} TL yatırıldı. Yeni bakiye: {self.__bakiye} TL")
        else:
            print("Lütfen geçerli bir miktar girin.")
    def para_çek(self, miktar):
        if miktar > 0 and miktar <= self.__bakiye:
            self.__bakiye -= miktar
            print(f"{miktar} TL çekildi. Yeni bakiye: {self.__bakiye} TL")
        else:
            print("Yetersiz bakiye veya geçersiz miktar.")