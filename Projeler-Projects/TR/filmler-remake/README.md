# Filmler API

Film ve yönetmen kayıtlarını yönetmek için FastAPI, SQLAlchemy ve PostgreSQL ile geliştirilmiş bir REST API.

## Özellikler

- Film ve yönetmen kayıtları oluşturma, listeleme, görüntüleme, güncelleme ve silme
- Film başlığı, türü, yayın yılı ve minimum puan ile filtreleme
- İstek ve yanıt verilerinin Pydantic ile doğrulanması
- Swagger arayüzü ve OpenAPI şeması
- Docker Compose ile API ve PostgreSQL'i birlikte çalıştırma

## Gereksinimler

Docker ile çalıştırmak için Docker ve Docker Compose gerekir. Yerel Python kurulumu için Python 3.12+ ve PostgreSQL 16 gerekir.

## Docker ile çalıştırma

Proje kök dizininde `.env.example` dosyasını `.env` olarak kopyalayın. Örnek ayarlar Docker Compose içindeki veritabanı servisine göre düzenlenmiştir:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/filmler_db
```

Ardından servisleri başlatın:

```bash
docker compose up --build
```

API `http://localhost:8000` adresinde kullanılabilir. Durdurmak için `Ctrl+C`, arka planda başlatılmış servisleri kapatmak için `docker compose down` komutunu çalıştırın. Veritabanı verileri `postgres_data` adlı Docker volume'ünde saklanır.

> Yerel geliştirmede `.env` içindeki `db` ana makine adını `localhost` olarak değiştirin. PostgreSQL'i ayrıca çalıştırıp `filmler_db` veritabanını oluşturun.

## Yerel Python kurulumu

Önce sanal ortam oluşturup bağımlılıkları yükleyin:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
Copy-Item .env.example .env
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
cp .env.example .env
pip install -r requirements.txt
```

Yerel PostgreSQL bağlantısını `.env` dosyasında belirtin. Örneğin:

```env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/filmler_db
```

Uygulamayı başlatın:

```bash
uvicorn app.main:app --reload
```

## API ve dokümantasyon

- `GET /` — API durum mesajı ve dokümantasyon yolu
- `GET /health` — Basit sağlık kontrolü
- `GET, POST /yonetmenler/` — Yönetmenleri listeleme ve oluşturma
- `GET, PATCH, DELETE /yonetmenler/{yonetmen_id}` — Yönetmen görüntüleme, güncelleme ve silme
- `GET, POST /filmler/` — Filmleri listeleme ve oluşturma
- `GET, PATCH, DELETE /filmler/{film_id}` — Film görüntüleme, güncelleme ve silme

Etkileşimli Swagger dokümantasyonu: `http://localhost:8000/docs`  
ReDoc dokümantasyonu: `http://localhost:8000/redoc`

### Film listeleme filtreleri

`GET /filmler/` aşağıdaki isteğe bağlı parametreleri kabul eder:

| Parametre | Açıklama |
| --- | --- |
| `arama` | Film başlığında metin araması |
| `tur` | Türe göre filtreleme |
| `yayin_yili` | Yayın yılına göre filtreleme |
| `min_puan` | Alt puan sınırı (0–10) |
| `skip` | Sayfalama için atlanacak kayıt sayısı (varsayılan: 0) |
| `limit` | Döndürülecek en fazla kayıt (varsayılan: 20, üst sınır: 100) |

Örnek: `GET /filmler/?arama=inception&min_puan=8&skip=0&limit=10`

Yönetmen listesi de `skip` ve `limit` parametrelerini destekler.

## Örnek istekler

Önce bir yönetmen oluşturun:

```bash
curl -X POST http://localhost:8000/yonetmenler/ \
  -H "Content-Type: application/json" \
  -d '{"ad_soyad":"Christopher Nolan","ulke":"Birleşik Krallık"}'
```

Oluşan yönetmenin `id` değerini film isteğinde kullanın:

```bash
curl -X POST http://localhost:8000/filmler/ \
  -H "Content-Type: application/json" \
  -d '{"baslik":"Inception","yayin_yili":2010,"tur":"Bilim Kurgu","sure_dakika":148,"puan":8.8,"ozet":"Rüyalar içinde rüya kurgulanan bir bilim kurgu filmi.","yonetmen_id":1}'
```

Film alanları: `baslik`, `yayin_yili`, `tur`, `sure_dakika`, `yonetmen_id`; `puan` ve `ozet` isteğe bağlıdır. Yayın yılı 1888–2100, süre 1–1000 dakika ve puan 0–10 aralığında olmalıdır. Film eklemek için önce ilgili yönetmen kaydı oluşturulmalıdır.

## Proje yapısı

```text
.
├── app/
│   ├── main.py              # FastAPI uygulaması ve genel uç noktalar
│   ├── database.py          # Veritabanı bağlantısı ve oturum yönetimi
│   ├── models.py            # SQLAlchemy modelleri
│   ├── schemas.py           # Pydantic istek/yanıt şemaları
│   └── routers/
│       ├── filmler.py       # Film uç noktaları
│       └── yonetmenler.py   # Yönetmen uç noktaları
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

Uygulama başlangıcında SQLAlchemy mevcut tabloları oluşturur. Bu yöntem tablo oluşturma ve başlangıç geliştirmesi içindir; mevcut tablolar üzerinde şema değişikliklerini otomatik olarak geçişe dönüştürmez.
