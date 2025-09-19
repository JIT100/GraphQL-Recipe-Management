#!/bin/sh
set -e

# Print environment type
echo "[entrypoint] Environment: ${DJANGO_SETTINGS_MODULE:-config.settings} (DEBUG=${DEBUG:-unset})"

# Optionally collect static files at startup
echo "[entrypoint] collecting static files"
if [ "${DEBUG}" = "True" ] || [ "${DEBUG}" = "true" ] || [ "${DEBUG}" = "1" ]; then
  
  python manage.py collectstatic --noinput || echo "[entrypoint] collectstatic failed (dev), continuing"
else
  python manage.py collectstatic --noinput
fi

echo "[entrypoint] starting: running migrations"
python manage.py migrate --noinput
echo "[entrypoint] migrations complete"

echo "[entrypoint] running create_demo_user (safe to run even if envs missing)"
python manage.py create_demo_user || true
echo "[entrypoint] create_demo_user finished"

echo "[entrypoint] handing off to container command"
exec "$@"
