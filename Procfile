web: bin/start-nginx gunicorn -c gunicorn.conf django_app.wsgi:application
worker: REMAP_SIGTERM=SIGQUIT celery -E -A -l error django_app worker
release: python manage.py migrate
