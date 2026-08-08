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
