# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev netcat-openbsd

COPY requirements.txt .
RUN pip install --upgrade pip --no-cache-dir -r requirements.txt

COPY . /app/

# Collect static files after the app is copied so Django can find static assets
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
