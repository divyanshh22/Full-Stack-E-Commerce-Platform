release: python manage.py migrate && python manage.py setup_site
web: gunicorn demo.wsgi:application --workers 2 --timeout 120
