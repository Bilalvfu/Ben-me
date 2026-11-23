# FastAPI Görev Yönetimi API

FastAPI, SQLAlchemy ve Pydantic ile geliştirilmiş, SQLite kullanan görev yönetimi REST API'si. Kullanıcı kaydı ve JWT ile giriş yapılır; görev uç noktaları giriş gerektirir.

## Özellikler

- Kullanıcı kaydı ve OAuth2 parola akışı üzerinden JWT token alma
- Görev oluşturma, listeleme, güncelleme ve silme
- SQLite veritabanı; tablolar uygulama başlarken oluşturulur
- Pytest ile otomatik testler

> **Veri erişimi:** Görevler kullanıcı hesabına bağlanmıyor. Giriş yapmış tüm kullanıcılar aynı görev listesini görüp görevleri güncelleyebilir veya silebilir. Bu davranış uygulama kodunun mevcut halidir.

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

Önce kullanıcı oluşturun, ardından `/token` adresine form verisiyle giriş yapıp token alın:

```bash
curl -X POST http://127.0.0.1:8000/register -H "Content-Type: application/json" -d '{"username":"ayse","password":"guclu-parola"}'
curl -X POST http://127.0.0.1:8000/token -H "Content-Type: application/x-www-form-urlencoded" -d "username=ayse&password=guclu-parola"
```

Token gerektiren görev isteklerine `Authorization: Bearer <token>` başlığını ekleyin.

## API uç noktaları

| Yöntem | Yol | Açıklama |
|---|---|---|
| `POST` | `/register` | Kullanıcı kaydı; JSON alanları `username`, `password` |
| `POST` | `/token` | Form alanlarıyla giriş; erişim tokenı döndürür |
| `POST` | `/tasks` | Görev oluşturur; `title`, isteğe bağlı `description` |
| `GET` | `/tasks` | Tüm görevleri listeler |
| `PUT` | `/tasks/{task_id}` | Görevin `title`, `description` ve/veya `completed` alanlarını günceller |
| `DELETE` | `/tasks/{task_id}` | Görevi siler |

Görev örneği:

```bash
curl -X POST http://127.0.0.1:8000/tasks -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"title":"Raporu hazırla","description":"İlk taslak"}'
curl http://127.0.0.1:8000/tasks -H "Authorization: Bearer <token>"
```

Yeni görevlerde `completed` varsayılan olarak `false` olur. Bulunmayan görev için güncelleme/silme yanıtı `404`'tür.

## Testler

```bash
pytest -q
```

Testler bellek içi SQLite veritabanı kullanır.

## Proje yapısı

```text
├── database.py    # SQLite bağlantısı ve oturum yönetimi
├── models.py      # User ve Task SQLAlchemy modelleri
├── schemas.py     # İstek/yanıt Pydantic şemaları
├── main.py        # Kimlik doğrulama ve görev uç noktaları
├── test_main.py   # Otomatik testler
├── tasks.db       # Yerel SQLite veritabanı (ilk çalıştırmada oluşur)
└── README.md
```

`main.py` içindeki JWT `SECRET_KEY` geliştirme amaçlı sabit bir değerdir. Gerçek dağıtımda gizli anahtarı ortam değişkeninden okuyacak şekilde yapılandırın.
.
