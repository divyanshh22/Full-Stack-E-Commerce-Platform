# Full-Stack E-Commerce Platform

A modern e-commerce web application built with **Django 4.2** and **PostgreSQL** — featuring a custom-built front-end (no Bootstrap), user authentication, a shopping cart, checkout flow, discount coupons, refund requests, and an admin dashboard.

> Developed by **Divyansh**

---

## Features

- 🛍️ **Product catalog** — 30 seeded products across 4 categories, each with photos, sale labels, and discount badges
- 🔍 **Product detail pages** with short/long descriptions
- 🛒 **Shopping cart** — add, remove, and adjust quantities (cart badge in the nav updates live)
- 💳 **Checkout flow** — billing/shipping addresses, payment options, and a Stripe payment screen
- 🎟️ **Discount coupons** with automatic cart/total recalculation
- 💬 **Refund requests** for placed orders
- 🔐 **Authentication** — sign up, sign in, password reset, and email management (allauth), with Django's built-in auth for login/logout
- 📦 **Admin dashboard** at `/admin/` — manage products, categories, slides, coupons, and orders
- 📱 **Responsive custom UI** — dark sticky nav, mobile menu, product cards, toasts, and a clean footer (no Bootstrap/jQuery)

## Tech Stack

| Layer      | Technology                          |
|------------|-------------------------------------|
| Backend    | Django 4.2, Python 3.10+            |
| Database   | PostgreSQL                          |
| Auth       | django-allauth + Django auth        |
| Payments   | Stripe (test keys)                  |
| Frontend   | Custom HTML/CSS/JS, Font Awesome, Google Fonts |
| Env        | python-dotenv (`.env` file)         |

## Getting Started

### Prerequisites

- **Python 3.10+**
- **PostgreSQL** running locally (or via a connection string)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/divyanshh22/Full-Stack-E-Commerce-Platform.git
cd Full-Stack-E-Commerce-Platform
```

### 2. Set up a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` and set at least the database credentials:

```env
DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

Create the database if it doesn't exist yet:

```sql
CREATE DATABASE ecommerce;
```

### 5. Migrate and seed sample data

```bash
python manage.py migrate
python manage.py seed_data   # adds 4 categories and 30 products with photos
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Useful Links

| Page                     | URL                                  |
|--------------------------|--------------------------------------|
| Shop (all products)      | `/shop/`                             |
| Your cart                | `/cart/`                             |
| Sign up                  | `/accounts/signup/`                  |
| Sign in                  | `/accounts/login/`                   |
| Admin panel              | `/admin/`                            |

## Commands

```bash
python manage.py seed_data          # seed categories + 30 products (idempotent)
python manage.py createsuperuser    # create an admin account
python manage.py check              # run Django system checks
python manage.py migrate            # apply database migrations
```

## Deploying to Render

The project ships with a `render.yaml` blueprint, a `Procfile`, and production-ready settings (WhiteNoise for static files, `DATABASE_URL` support, env-driven config) — so deploying is mostly one click.

### One-click deploy (blueprint)

1. Push this repository to GitHub (already done).
2. Go to https://dashboard.render.com and click **New → Blueprint**.
3. Select the `Full-Stack-E-Commerce-Platform` repo.
4. Render reads `render.yaml`, creates the free PostgreSQL database (`ecommerce-db`) and web service (`full-stack-e-commerce-platform-6gy3`), and auto-generates `SECRET_KEY`.
5. Click **Apply**. Render builds the app, collects static files, runs migrations + setup, and seeds data before starting the web service.

### Manual setup (dashboard fields)

If you created the service manually, use these fields:

**Build command:**
```
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate && python manage.py setup_site && python manage.py ensure_superuser
```

**Start command:**
```
python manage.py seed_data && gunicorn demo.wsgi:application --workers 2 --timeout 120
```

**Release command** (only if your dashboard shows a Release Command field — otherwise skip; the build command already runs migrations):
```
python manage.py migrate && python manage.py setup_site && python manage.py ensure_superuser
```

### After the first deploy

Set these env vars on the web service (Dashboard → full-stack-e-commerce-platform-6gy3 → Environment):

| Key                 | Value                                                    |
|---------------------|----------------------------------------------------------|
| `STRIPE_PUBLIC_KEY` | your Stripe publishable test key (optional)              |
| `STRIPE_SECRET_KEY` | your Stripe secret test key (optional)                   |
| `ADMIN_USERNAME`    | admin (optional) — superuser created automatically       |
| `ADMIN_PASSWORD`    | your admin password (optional)                           |
| `ADMIN_EMAIL`       | your email (optional)                                    |

On every deploy the **release command** automatically runs `migrate`, `setup_site`, `ensure_superuser` (creates the admin from `ADMIN_*` vars if missing), and `seed_data` (30 sample products). No Shell access is required — but the interactive Shell needs a paid plan anyway.

> The app is live at `https://full-stack-e-commerce-platform-6gy3.onrender.com`.

### Notes about the Render free tier

- Free web services **spin down after 15 minutes** of inactivity and take ~1 minute to wake up on the next request.
- Free PostgreSQL databases are limited to **1 GB** and **expire after 30 days** (upgrade to a paid instance to keep the data).
- Uploaded images are stored on a 1 GB persistent disk mounted at `media_root`.

## Configuration Notes

- **Emails** are printed to the console (`EMAIL_BACKEND = console`) and email verification is disabled, so sign-up works out of the box without an SMTP server.
- **Stripe keys** are test keys — set your own in `.env` (`STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`) to process real payments.
- The local database is **PostgreSQL**; SQLite support was removed. Secrets never live in the repository — everything sensitive is read from `.env` (gitignored).

## Project Structure

```
├── core/                  # Main app: models, views, urls, forms, admin
│   └── management/commands/
│       └── seed_data.py   # Seeds categories and products
├── demo/                  # Project settings, URLs, WSGI
├── static_in_env/         # CSS, JS, images, fonts (served statically)
├── templates/             # Django templates (base, shop, checkout, accounts, ...)
├── media_root/            # Uploaded product images (gitignored)
├── .env.example           # Template for local environment config
└── manage.py
```

## License

This project is for educational purposes. Original template by [Colorlib](https://colorlib.com).
