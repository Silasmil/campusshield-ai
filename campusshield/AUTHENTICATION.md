# CampusShield AI - Login & Authentication Guide

## 🛡️ Default Login Credentials

### Admin Account (for initial access)
```
Username: admin
Password: CampusShield123!
Email: admin@campusshield.local
```

### How to Use These Credentials

1. **Start the server:**
   ```powershell
   cd c:\Development\campusshield-ai\campusshield
   .\start_server.ps1
   ```

2. **Open browser:**
   ```
   http://localhost:8000
   ```

3. **Login with:**
   - Username: `admin`
   - Password: `CampusShield123!`

4. **Access the dashboard:**
   - You'll be redirected to the dashboard after login

---

## 🔐 Password Change Feature

### For Users
Your login page now has a **"Change Password"** link:

1. Go to: http://localhost:8000/accounts/login/
2. Click **"Change Password"** link
3. Enter your **old password**
4. Enter your **new password** (twice to confirm)
5. Click **"Change Password"** button
6. You'll be redirected to a success page

### Direct URL Access
```
http://localhost:8000/accounts/password_change/
```

---

## 👥 Creating Additional Users

### Via Django Shell
```powershell
cd c:\Development\campusshield-ai\campusshield
.\venv\Scripts\Activate.ps1
python manage.py shell
```

Then in the shell:
```python
from django.contrib.auth.models import User

# Create a new staff user
User.objects.create_user(
    username='security_analyst',
    email='analyst@campusshield.local',
    password='SecurePassword123!'
)

# Create a superuser
User.objects.create_superuser(
    username='admin2',
    email='admin2@campusshield.local',
    password='AdminPass123!'
)

exit()
```

### Via Django Admin
1. Login to admin: http://localhost:8000/admin/
2. Click **"Users"** → **"Add User"**
3. Enter username and password
4. Click **"Save"**

---

## 📋 Available URLs

| URL | Purpose | Requires Login |
|-----|---------|---|
| `/` | Dashboard | ✅ Yes |
| `/accounts/login/` | Login Page | ❌ No |
| `/accounts/logout/` | Logout | ✅ Yes |
| `/accounts/password_change/` | Change Password | ✅ Yes |
| `/accounts/password_change/done/` | Success Page | ✅ Yes |
| `/admin/` | Django Admin | ✅ Yes (Superuser) |
| `/incidents/` | Incidents List | ✅ Yes |

---

## 🔑 Password Requirements

Django enforces these password rules:
- ❌ Cannot be too similar to username
- ❌ Cannot be all numeric
- ❌ Cannot be a common password
- ✅ Should be at least 8 characters
- ✅ Should contain mix of letters, numbers, symbols

---

## 🚨 If You Forgot Your Password

### Option 1: Reset via Django Shell
```powershell
.\venv\Scripts\Activate.ps1
python manage.py shell
```

```python
from django.contrib.auth.models import User

user = User.objects.get(username='admin')
user.set_password('NewPassword123!')
user.save()
exit()
```

### Option 2: Create Script
Use the `create_user.py` script to reset:
```powershell
python create_user.py
```

---

## 🔒 Security Notes

**For Development Only:**
- Default password is set intentionally for testing
- Change it immediately in production
- Use strong, unique passwords
- Enable HTTPS in production
- Set DJANGO_SECRET_KEY environment variable

**Environment Variables:**
```powershell
# Set in production
$env:DJANGO_SECRET_KEY = "your-long-random-secret-key"
$env:DJANGO_DEBUG = "False"
```

---

## 📁 Related Files

- Login template: `templates/registration/login.html`
- Password change: `templates/registration/password_change.html`
- Success page: `templates/registration/password_change_done.html`
- User creation: `create_user.py`
- URL config: `campusshield/urls.py`

---

## ✅ Testing Login

After creating the user, test the login flow:

1. **Login:** http://localhost:8000/accounts/login/
2. **Dashboard:** http://localhost:8000/ (auto-redirects if logged in)
3. **Change Password:** Click link on login page
4. **Logout:** Click logout button in dashboard
5. **Login again:** Verify new password works

---

**Admin credentials created successfully!** ✅
Use the provided credentials to access your dashboard.
