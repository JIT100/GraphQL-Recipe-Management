import os
from django.core.wsgi import get_wsgi_application

# Use the consolidated settings selector; it switches based on DEBUG env
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
application = get_wsgi_application()
