release: python manage.py migrate && python manage.py setup_site && python manage.py ensure_superuser && python manage.py seed_data
web: gunicorn demo.wsgi:application --workers 2 --timeout 120
