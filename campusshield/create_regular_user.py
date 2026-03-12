#!/usr/bin/env python
"""
Create regular user account for CampusShield AI
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'campusshield.settings')
django.setup()

from django.contrib.auth.models import User

# Create regular user (not superuser/admin)
username = 'testuser'
email = 'testuser@campusshield.local'
password = 'TestUser123!'

try:
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"✅ Regular user '{username}' password updated")
except User.DoesNotExist:
    user = User.objects.create_user(username, email, password)
    print(f"✅ Regular user '{username}' created successfully")

print(f"\n📋 Login Credentials (Regular User):")
print(f"   Username: {username}")
print(f"   Password: {password}")
print(f"   Email: {email}")
print(f"   Admin Access: No")
print(f"\n✅ You can now login as a normal user (not admin)")
