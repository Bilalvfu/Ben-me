CREATE TABLE kitaplar (
    isbn INTEGER PRIMARY KEY,
    ad TEXT NOT NULL,
    yazar TEXT NOT NULL,
    sayfa_sayisi INTEGER NOT NULL
);

CREATE TABLE kullanıcılar (
    id INTEGER PRIMARY KEY,
    ad TEXT NOT NULL,
    soyad TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);
SELECT kullanıcılar.ad, siparisler.urun_adi 
FROM siparisler 
JOIN kullanıcılar ON siparisler.kullanici_id = kullanıcılar.id 
INSERT INTO kitaplar (isbn, ad, yazar, sayfa_sayisi) VALUES (123456789, 'Suç ve Ceza', 'Fyodor Dostoyevski', 250);
UPDATE kitaplar SET sayfa_sayisi = 300 WHERE isbn = 123456789;
DELETE FROM kitaplar WHERE sayfa_sayisi < 100;