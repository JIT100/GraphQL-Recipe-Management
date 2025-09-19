#!/bin/sh
set -e

echo "[app] DEBUG=${DEBUG:-unset}"
echo "[app] collectstatic"
if [ "${DEBUG}" = "True" ] || [ "${DEBUG}" = "true" ] || [ "${DEBUG}" = "1" ]; then
  python manage.py collectstatic --noinput || echo "[app] collectstatic failed; continuing"
else
  python manage.py collectstatic --noinput
fi

echo "[app] migrate"
python manage.py migrate --noinput

python manage.py create_demo_user || true

exec "$@"
