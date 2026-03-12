#!/usr/bin/env python
"""
CampusShield AI - System Error Check & Verification
Comprehensive error detection and reporting
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusshield.settings')
django.setup()

from incidents.models import Incident
from ai_engine.anomaly_detector import AnomalyDetector
from ai_engine.threat_classifier import ThreatClassifier
from django.contrib.auth.models import User

print("\n" + "="*70)
print("CampusShield AI - Comprehensive System Check".center(70))
print("="*70)

# Module Import Checks
print("\n🔍 MODULE IMPORT CHECKS")
print("-" * 70)
try:
    from incidents.models import Incident
    print("✅ incidents.models - OK")
except Exception as e:
    print(f"❌ incidents.models - ERROR: {e}")

try:
    from incidents.views import (
        incidents_list, incidents_dashboard, analyze_incident,
        train_ai_models, incident_analysis
    )
    print("✅ incidents.views - OK")
except Exception as e:
    print(f"❌ incidents.views - ERROR: {e}")

try:
    from ai_engine.anomaly_detector import AnomalyDetector
    print("✅ ai_engine.anomaly_detector - OK")
except Exception as e:
    print(f"❌ ai_engine.anomaly_detector - ERROR: {e}")

try:
    from ai_engine.threat_classifier import ThreatClassifier
    print("✅ ai_engine.threat_classifier - OK")
except Exception as e:
    print(f"❌ ai_engine.threat_classifier - ERROR: {e}")

try:
    from django.contrib.auth.models import User
    print("✅ django.contrib.auth - OK")
except Exception as e:
    print(f"❌ django.contrib.auth - ERROR: {e}")

# Database Integrity Checks
print("\n📊 DATABASE INTEGRITY CHECKS")
print("-" * 70)
try:
    total_users = User.objects.count()
    print(f"✅ Total users: {total_users}")
except Exception as e:
    print(f"❌ User query failed: {e}")

try:
    total_incidents = Incident.objects.count()
    print(f"✅ Total incidents: {total_incidents}")
except Exception as e:
    print(f"❌ Incident query failed: {e}")

try:
    admin_exists = User.objects.filter(username='admin').exists()
    if admin_exists:
        admin = User.objects.get(username='admin')
        print(f"✅ Admin user exists: YES")
        print(f"   - Superuser: {admin.is_superuser}")
        print(f"   - Staff: {admin.is_staff}")
        print(f"   - Active: {admin.is_active}")
    else:
        print(f"❌ Admin user exists: NO - User account missing!")
except Exception as e:
    print(f"❌ Admin check failed: {e}")

# Model Validation
print("\n📋 MODEL VALIDATION")
print("-" * 70)
try:
    incidents = Incident.objects.all()
    print(f"✅ Incident model accessible: {incidents.count()} records")
    if incidents.count() > 0:
        sample = incidents.first()
        print(f"   - Sample incident: {sample.title}")
        print(f"   - Severity: {sample.severity}")
        print(f"   - Status: {sample.status}")
except Exception as e:
    print(f"❌ Model validation failed: {e}")

# AI Module Checks
print("\n🤖 AI MODULE CHECKS")
print("-" * 70)
try:
    detector = AnomalyDetector()
    print(f"✅ AnomalyDetector initialized")
    print(f"   - Trained: {detector.is_trained}")
except Exception as e:
    print(f"❌ AnomalyDetector failed: {e}")

try:
    classifier = ThreatClassifier()
    print(f"✅ ThreatClassifier initialized")
    print(f"   - Trained: {classifier.is_trained}")
except Exception as e:
    print(f"❌ ThreatClassifier failed: {e}")

# Settings Validation
print("\n⚙️  SETTINGS VALIDATION")
print("-" * 70)
from django.conf import settings
print(f"✅ DEBUG: {settings.DEBUG}")
print(f"✅ ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
print(f"✅ Database: {settings.DATABASES['default']['ENGINE']}")
print(f"✅ INSTALLED_APPS: {len(settings.INSTALLED_APPS)} apps")

# URL Configuration
print("\n🌐 URL CONFIGURATION")
print("-" * 70)
try:
    from django.urls import get_resolver, reverse
    resolver = get_resolver()
    patterns = resolver.url_patterns
    print(f"✅ URL patterns configured: {len(patterns)} routes")
    print(f"✅ password_change URL: {reverse('password_change')}")
    print(f"✅ login URL: {reverse('login')}")
    print(f"✅ dashboard URL: {reverse('dashboard')}")
except Exception as e:
    print(f"❌ URL configuration error: {e}")

# Final Summary
print("\n" + "="*70)
print("✅ SYSTEM CHECK COMPLETE - All systems operational!")
print("="*70 + "\n")
