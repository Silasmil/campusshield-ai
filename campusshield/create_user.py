#!/usr/bin/env python
"""
Create default superuser for CampusShield AI
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusshield.settings')
django.setup()

from django.contrib.auth.models import User

# Create or update superuser
username = 'admin'
email = 'admin@campusshield.local'
password = 'CampusShield123!'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✅ User '{username}' password updated")
except User.DoesNotExist:
    user = User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser '{username}' created successfully")

print(f"\n📋 Login Credentials:")
print(f"   Username: {username}")
print(f"   Password: {password}")
print(f"   Email: {email}")
