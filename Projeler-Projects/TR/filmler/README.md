# Filmler API

Kullanıcıların kendi film koleksiyonlarını yönetebildiği, FastAPI ve SQLite tabanlı REST API. Kimlik doğrulama JWT Bearer token ile yapılır; her kullanıcı yalnızca kendi filmlerine erişebilir.

## Özellikler

- Kullanıcı kaydı ve parola ile giriş
- JWT ile korunan film işlemleri
- Film ekleme, listeleme, detay görüntüleme, güncelleme ve silme
- Film listesini türe (`genre`) ve izlenme durumuna (`watched`) göre filtreleme
- Kullanıcı bazlı film erişimi
- Pytest ile otomatik testler

## Gereksinimler

- Python 3.10 veya üzeri

## Kurulum ve çalıştırma

Proje klasöründe sanal ortam oluşturup etkinleştirin, ardından bağımlılıkları yükleyin:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install fastapi "uvicorn[standard]" sqlalchemy pydantic "python-jose[cryptography]" passlib pytest httpx python-multipart
uvicorn main:app --reload
```

Sunucu `http://127.0.0.1:8000` adresinde açılır. İnteraktif API belgeleri: `http://127.0.0.1:8000/docs`.

## Kimlik doğrulama

Önce kullanıcı kaydı yapın. `/token` uç noktasına form verisi göndererek JWT alın. Korumalı isteklerde tokenı `Authorization: Bearer <token>` başlığıyla iletin.

```bash
curl -X POST http://127.0.0.1:8000/register -H "Content-Type: application/json" -d '{"username":"ayse","password":"guclu-parola"}'
curl -X POST http://127.0.0.1:8000/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=ayse&password=guclu-parola"
```

## API uç noktaları

| Yöntem | Yol | Açıklama |
|---|---|---|
| `POST` | `/register` | Kullanıcı kaydı; JSON alanları `username`, `password` |
| `POST` | `/token` | Form alanlarıyla giriş; erişim tokenı döndürür |
| `POST` | `/movies/` | Film ekler: `title`, `director`, `release_year`, `genre`, isteğe bağlı `watched` |
| `GET` | `/movies/` | Oturum açmış kullanıcının filmlerini listeler; `genre` ve `watched` filtreleri alır |
| `GET` | `/movies/{movie_id}` | Kullanıcının bir filminin ayrıntısını getirir |
| `PUT` | `/movies/{movie_id}` | Film alanlarının gönderilen kısmını günceller |
| `DELETE` | `/movies/{movie_id}` | Kullanıcının filmini siler |

Örnek film ekleme ve filtreli listeleme:

```bash
curl -X POST http://127.0.0.1:8000/movies/ -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title":"Interstellar","director":"Christopher Nolan","release_year":2014,"genre":"Sci-Fi","watched":true}'
curl "http://127.0.0.1:8000/movies/?genre=sci-fi&watched=true" -H "Authorization: Bearer <token>"
```

`genre` araması büyük/küçük harfe duyarsız kısmi eşleşme yapar. `watched` değeri `true` veya `false` olabilir. `watched` gönderilmezse yeni film varsayılan olarak izlenmemiş (`false`) kaydedilir. Başka kullanıcıya ait veya bulunmayan film için detay/güncelleme/silme yanıtı `404`'tür.

## Testler

```bash
pytest -q
```

Testler bellek içi SQLite veritabanı kullanır.

## Proje yapısı

```text
├── database.py    # SQLite bağlantısı ve oturum yönetimi
├── models.py      # User ve Movie SQLAlchemy modelleri
├── schemas.py     # İstek/yanıt Pydantic şemaları
├── main.py        # Kimlik doğrulama ve film uç noktaları
├── test_main.py   # Otomatik testler
├── films.db       # Yerel SQLite veritabanı (ilk çalıştırmada oluşur)
└── README.md
```

`main.py` içindeki JWT `SECRET_KEY` geliştirme amaçlı sabit bir değerdir. Gerçek dağıtımda gizli anahtarı ortam değişkeninden okuyacak şekilde yapılandırın.
.
