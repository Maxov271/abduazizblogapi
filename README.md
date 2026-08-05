# Hanzo-Dev — Django REST API + HTML/CSS/JS frontend

## Arxitektura

- **Backend**: Django + Django REST Framework — faqat `/api/*` va `/admin/*` ni beradi (JSON API).
- **Frontend**: sof HTML/CSS/JS (`frontend/` papkasi) — bitta `index.html`, ichki
  navigatsiya (About/Resume/Portfolio/Thread) `hash router` (`#/about`, `#/portfolio/slug`
  va h.k.) orqali, ma'lumotlar `fetch()` bilan API'dan olinadi. Server-side render yo'q.
- Django development rejimida frontend'ni ham xuddi shu domenda xizmat qiladi
  (`hanzodev_site/urls.py`dagi SPA fallback), lekin frontend istasangiz butunlay
  boshqa static hosting'ga (Netlify, Nginx va h.k.) ham ko'chirib qo'yish mumkin —
  faqat `frontend/static/js/api.js` ichidagi `API_BASE`ni to'liq API manzilga
  o'zgartirasiz va Django tomonda CORS sozlaysiz.

## Papkalar

```
hanzodev_site/
  hanzodev_site/     # Django settings, urls, wsgi
  core/               # models, admin, serializers, API view'lar
    models.py
    serializers.py
    api_views.py
    api_urls.py
    admin.py
    telegram.py       # Telegram bot bildirishnomalari
  frontend/           # sof HTML/CSS/JS
    index.html
    static/css/style.css
    static/js/api.js  # backend bilan aloqa
    static/js/app.js  # router + render funksiyalari
```

## API endpointlar (`/api/...`)

| Endpoint | Metod | Tavsif |
|---|---|---|
| `/api/site-settings/` | GET | favicon, sayt nomi, rang, fon rasmi |
| `/api/profile/` | GET | ism, rasm, tel, email, manzil, about matni |
| `/api/social-links/` | GET | ijtimoiy tarmoqlar |
| `/api/services/` | GET | "What I Do" kartalari |
| `/api/inside-world/` | GET | "Inside ... World" kartalari |
| `/api/skills/` | GET | Resume "My Skills" |
| `/api/journey/` | GET | Resume "My Journey" |
| `/api/portfolio-categories/` | GET | filter tab'lari |
| `/api/portfolio/?category=slug` | GET | loyihalar ro'yxati |
| `/api/portfolio/<slug>/` | GET | bitta loyiha |
| `/api/thread/` | GET | blog postlari |
| `/api/thread/<slug>/` | GET | bitta post |
| `/api/thread/<slug>/comments/` | GET | tasdiqlangan izohlar |
| `/api/thread/<slug>/comments/create/` | POST | yangi izoh (`name` majburiy) — `pending` holatda saqlanadi, Telegramga xabar boradi |
| `/api/contact/` | POST | kontakt formasi — Telegramga xabar boradi |

## O'rnatish

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # to'ldiring
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo         # (ixtiyoriy) boshlang'ich yozuvlar
python manage.py collectstatic --noinput
python manage.py runserver
```

Sayt: http://127.0.0.1:8000/  (frontend shu yerda, API'ga fetch qiladi)
API: http://127.0.0.1:8000/api/
Admin: http://127.0.0.1:8000/admin/

## Telegram bot sozlash

1. **@BotFather**'da `/newbot` — token oling.
2. Botga `/start` yozing.
3. `https://api.telegram.org/bot<TOKEN>/getUpdates` sahifasidan `chat_id` toping.
4. `.env`: `TELEGRAM_BOT_TOKEN=...`, `TELEGRAM_CHAT_ID=...`
   (yoki admin panel → Site sozlamalari)

## Frontend'ni alohida joylashtirmoqchi bo'lsangiz

`frontend/static/js/api.js` faylida:
```js
const API_BASE = "https://api.hanzodev.uz/api";
```
deb o'zgartiring, `frontend/` papkasini istalgan static hosting'ga yuklang,
va Django tomonda `.env`da:
```
CORS_ALLOWED_ORIGINS=https://hanzodev.uz
CORS_ALLOW_ALL_ORIGINS=False
```

## Alwaysdata'ga joylash

- **Application path**: `.../hanzodev_site/hanzodev_site` (wsgi.py joylashgan joy)
- **Working directory**: `.../hanzodev_site/`
- **virtualenv directory**: `.../hanzodev_site/venv/`
- **Static paths**: `/static/=.../hanzodev_site/staticfiles/`, `/media/=.../hanzodev_site/media/`
- Serverda: `pip install -r requirements.txt`, `.env` to'ldirish, `migrate`,
  `collectstatic`, `createsuperuser`

## Admin panelda to'ldirish tartibi

1. Profil (ism, rasm, tel, email, manzil, about matni)
2. Site sozlamalari (favicon, rang, fon rasmi)
3. Ijtimoiy tarmoqlar
4. Xizmatlar (What I Do)
5. Inside World kartalari
6. Skill guruhlari, My Journey
7. Portfolio kategoriyalari va loyihalar
8. Thread postlari
9. Izohlar — kelganlarini tasdiqlang, shundagina saytda chiqadi

## Admin panel (API-based, alohida domenlar uchun)

Bu loyihada **ikki xil admin bor**:

1. **Django o'zining ichki admin paneli** — `https://devopsurol.alwaysdata.net/admin/`
   (yoki backend joylashgan domen). Bu sessiya/cookie asosida ishlaydi, backend
   bilan bir xil domenda turadi, faqat zaxira/texnik vosita sifatida qoladi.

2. **Sizning sayt dizayningizga mos SPA admin panel** — frontend qaysi domenda
   bo'lsa (`https://umarovgroup.uz`), o'sha domenda **`/admin`** manzilida ochiladi:
   `https://umarovgroup.uz/admin`. Bu **token-based** autentifikatsiya bilan ishlaydi
   (`Authorization: Token ...` header), shuning uchun frontend va backend turli
   domenlarda bo'lsa ham **xavfsiz** — cookie/CSRF muammosi umuman yo'q.

### Ishlash tartibi

- `POST /api/auth/login/` — login+parol yuborilsa, **faqat `is_staff=True`**
  foydalanuvchiga token qaytaradi (`python manage.py createsuperuser` bilan
  yaratilgan hisob ishlaydi)
- Token brauzer `localStorage`da saqlanadi, har bir keyingi so'rovda header orqali yuboriladi
- Barcha yozish (`POST/PATCH/DELETE`) endpointlari `/api/admin/...` da,
  `IsStaffUser` permission bilan himoyalangan — token bo'lmasa yoki `is_staff=False`
  bo'lsa 401/403 qaytadi
- O'qish uchun ochiq API (`/api/site-settings/`, `/api/portfolio/` va h.k.) — o'zgarishsiz

### Netlify'ga joylashda muhim

`frontend/_redirects` fayli bor — bu Netlify'ga "qaysi yo'l kelsa ham `index.html`ni
qaytar" deb aytadi. Shu fayl bo'lmasa, `umarovgroup.uz/admin`ga to'g'ridan-to'g'ri
kirganda 404 chiqadi (chunki bu haqiqiy fayl emas, JS orqali ishlaydigan yo'l).
`frontend/` papkasini Netlify'ga yuklaganda `_redirects` ham albatta ko'chishi kerak.

### CORS sozlash

`.env`da (backend tomonda):
```
CORS_ALLOWED_ORIGINS=https://umarovgroup.uz,https://www.umarovgroup.uz
CORS_ALLOW_ALL_ORIGINS=False
```
Domen aktivlashgach shu qatorni to'ldiring — hozircha Netlify test-manzilingizni
(`https://xxxx.netlify.app`) ham shu ro'yxatga qo'shib turing.

### API manzilini frontend'da sozlash

`frontend/static/js/api.js`:
```js
const API_BASE = "https://devopsurol.alwaysdata.net/api";
```
(hozir sizda shu manzilga ulangan bo'lsa, o'zgartirish shart emas)
