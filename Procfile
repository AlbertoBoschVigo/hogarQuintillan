release: python manage.py migrate
web: bin/start-pgbouncer-stunnel daphne hogarQuintillan.asgi:application --port $PORT --bind 0.0.0.0