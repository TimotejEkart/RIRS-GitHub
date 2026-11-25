#!/bin/sh
set -e
cd backend
python manage.py migrate --noinput
python manage.py loaddata zacetni_podatki
exec gunicorn karrabimzagym.wsgi --bind "0.0.0.0:${PORT:-8080}" --workers 2
