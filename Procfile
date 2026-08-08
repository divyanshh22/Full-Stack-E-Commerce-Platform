release: python manage.py migrate && python manage.py setup_site && python manage.py ensure_superuser
web: python manage.py seed_data && gunicorn demo.wsgi:application --workers 2 --timeout 120
