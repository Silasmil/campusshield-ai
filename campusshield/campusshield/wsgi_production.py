"""
WSGI config for campusshield project in production.
For production deployment with Gunicorn, uWSGI, or similar.

Usage:
  gunicorn campusshield.wsgi:application --workers 4 --bind 0.0.0.0:8000
  uwsgi --http :8000 --wsgi-file campusshield/wsgi.py --master --processes 4
"""

import os
import sys
from pathlib import Path

# Add project to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusshield.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application

# Get the WSGI application
application = get_wsgi_application()

# Additional production middleware wrapping (optional)
from django.middleware.wsgi import WSGIServerError

class ProductionWSGIApplication:
    """Wrapper for production WSGI with error handling"""
    
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except Exception as e:
            # Log errors for monitoring
            import logging
            logger = logging.getLogger('django')
            logger.exception("Unhandled WSGI exception")
            
            # Return 500 error response
            response = [b'Internal Server Error']
            start_response('500 Internal Server Error', [
                ('Content-Type', 'text/plain'),
                ('Content-Length', str(len(response[0])))
            ])
            return response

# Uncomment to enable production wrapper
# application = ProductionWSGIApplication(application)
