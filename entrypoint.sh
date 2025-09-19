#!/bin/sh
set -e

echo "[entrypoint] starting: running migrations"
python manage.py migrate --noinput
echo "[entrypoint] migrations complete"

echo "[entrypoint] running create_demo_user (safe to run even if envs missing)"
python manage.py create_demo_user || true
echo "[entrypoint] create_demo_user finished"

echo "[entrypoint] handing off to container command"
exec "$@"
