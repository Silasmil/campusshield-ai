#!/usr/bin/env python
"""
HTTPS development server wrapper for Django
Allows running the development server with SSL for testing HTTPS locally
"""
import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "campusshield.settings")
    
    # Set environment variables for development
    os.environ.setdefault("DJANGO_DEBUG", "True")
    
    try:
        from django.core.management.commands.runserver import Command as RunServerCommand
        
        # Try to use runserver_plus with SSL if django-extensions is available
        try:
            execute_from_command_line([
                'manage.py',
                'runserver_plus',
                '--cert', 'ssl_certs/cert.pem',
                '--key', 'ssl_certs/key.pem',
                '0.0.0.0:8000'
            ])
        except (ImportError, SystemExit):
            # Fall back to regular runserver
            print("\n⚠️ django-extensions not found. Run 'pip install django-extensions' for HTTPS support")
            print("Starting regular HTTP development server...\n")
            execute_from_command_line([
                'manage.py',
                'runserver',
                '0.0.0.0:8000'
            ])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
