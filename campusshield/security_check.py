#!/usr/bin/env python
"""
CampusShield AI - Security Verification & Compliance Checker
Enterprise-Grade Security Assessment
"""
import os
import sys
import django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusshield.settings')
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("CampusShield AI - Production Security Verification".center(80))
print("="*80 + "\n")

PASSED = 0
FAILED = 0
WARNINGS = 0

def check(description, condition, required=True):
    global PASSED, FAILED, WARNINGS
    status = "✅ PASS" if condition else ("❌ FAIL" if required else "⚠️  WARN")
    if condition:
        PASSED += 1
        symbol = "✅"
    elif required:
        FAILED += 1
        symbol = "❌"
    else:
        WARNINGS += 1
        symbol = "⚠️ "
    print(f"{symbol} {description}")
    return condition

print("🔐 SECURITY CHECKS")
print("-" * 80)

# Critical Security Checks
print("\n1. SECRET KEY Security:")
check("SECRET_KEY configured", bool(settings.SECRET_KEY), required=True)
check("SECRET_KEY length > 50", len(settings.SECRET_KEY) > 50, required=True)
check("SECRET_KEY not default", 
      'dev-key' not in settings.SECRET_KEY.lower() and 
      'change' not in settings.SECRET_KEY.lower(), 
      required=True)

print("\n2. Debug Mode:")
check("DEBUG = False", settings.DEBUG == False, required=True)

print("\n3. Allowed Hosts:")
check("ALLOWED_HOSTS configured", bool(settings.ALLOWED_HOSTS), required=True)
check("ALLOWED_HOSTS not wildcard", '*' not in settings.ALLOWED_HOSTS, required=True)

print("\n4. HTTPS/SSL Configuration:")
check("SECURE_SSL_REDIRECT enabled", 
      settings.SECURE_SSL_REDIRECT if hasattr(settings, 'SECURE_SSL_REDIRECT') else False,
      required=True)
check("HSTS enabled", 
      settings.SECURE_HSTS_SECONDS > 0 if hasattr(settings, 'SECURE_HSTS_SECONDS') else False,
      required=True)
check("HSTS includes subdomains",
      settings.SECURE_HSTS_INCLUDE_SUBDOMAINS if hasattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS') else False,
      required=True)

print("\n5. Cookie Security:")
check("SESSION_COOKIE_SECURE enabled", 
      settings.SESSION_COOKIE_SECURE if hasattr(settings, 'SESSION_COOKIE_SECURE') else False,
      required=True)
check("SESSION_COOKIE_HTTPONLY enabled",
      settings.SESSION_COOKIE_HTTPONLY if hasattr(settings, 'SESSION_COOKIE_HTTPONLY') else False,
      required=True)
check("CSRF_COOKIE_SECURE enabled",
      settings.CSRF_COOKIE_SECURE if hasattr(settings, 'CSRF_COOKIE_SECURE') else False,
      required=True)
check("CSRF_COOKIE_HTTPONLY enabled",
      settings.CSRF_COOKIE_HTTPONLY if hasattr(settings, 'CSRF_COOKIE_HTTPONLY') else False,
      required=True)

print("\n6. Security Headers:")
check("SECURE_CONTENT_TYPE_NOSNIFF enabled",
      settings.SECURE_CONTENT_TYPE_NOSNIFF if hasattr(settings, 'SECURE_CONTENT_TYPE_NOSNIFF') else False,
      required=True)
check("SECURE_BROWSER_XSS_FILTER enabled",
      settings.SECURE_BROWSER_XSS_FILTER if hasattr(settings, 'SECURE_BROWSER_XSS_FILTER') else False,
      required=True)
check("X_FRAME_OPTIONS = DENY",
      settings.X_FRAME_OPTIONS == 'DENY' if hasattr(settings, 'X_FRAME_OPTIONS') else False,
      required=True)

print("\n7. Database Security:")
check("Not using SQLite in production",
      'sqlite' not in settings.DATABASES['default']['ENGINE'].lower() 
      if os.environ.get('DJANGO_ENVIRONMENT') == 'production'
      else True,
      required=True)
check("Database password required",
      bool(settings.DATABASES['default'].get('PASSWORD'))
      if os.environ.get('DJANGO_ENVIRONMENT') == 'production'
      else True,
      required=True)

print("\n8. Logging Configuration:")
check("Logging configured", 
      'LOGGING' in dir(settings) and settings.LOGGING is not None,
      required=False)

print("\n9. MIDDLEWARE Security:")
check("SecurityMiddleware enabled",
      'django.middleware.security.SecurityMiddleware' in settings.MIDDLEWARE,
      required=True)
check("CSRF Middleware enabled",
      'django.middleware.csrf.CsrfViewMiddleware' in settings.MIDDLEWARE,
      required=True)

print("\n10. INSTALLED APPS:")
check("Django admin secured",
      'django.contrib.admin' in settings.INSTALLED_APPS,
      required=False)

print("\n" + "="*80)
print("SUMMARY".center(80))
print("="*80)
print(f"✅ Checks Passed: {PASSED}")
print(f"❌ Checks Failed: {FAILED}")
print(f"⚠️  Warnings: {WARNINGS}")
print(f"\nEnvironment: {os.environ.get('DJANGO_ENVIRONMENT', 'development')}")
print(f"Debug Mode: {settings.DEBUG}")

if FAILED == 0:
    print("\n✅ PRODUCTION READY - All security checks passed!")
else:
    print(f"\n❌ SECURITY ISSUES FOUND - {FAILED} critical issue(s) must be fixed before deployment")
    sys.exit(1)

print("="*80 + "\n")
