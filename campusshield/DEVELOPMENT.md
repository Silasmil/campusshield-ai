# CampusShield AI - Development Setup Guide

## Quick Start

### Option 1: Using PowerShell Script (Recommended)
```powershell
cd c:\Development\campusshield-ai\campusshield
.\start_server.ps1
```

### Option 2: Manual Setup
```powershell
cd c:\Development\campusshield-ai\campusshield
.\venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

### Option 3: Using Batch Script
```cmd
cd c:\Development\campusshield-ai\campusshield
run_server.bat
```

## Accessing the Application

Once the server is running, open your browser and go to:

**http://localhost:8000**

Or specifically:

**http://127.0.0.1:8000**

### Default Behavior
- The development server runs on **port 8000**
- All HTTP traffic is accepted (no forced HTTPS in development)
- Django debug mode is enabled for development
- Static files are automatically served

## System Architecture

### Backend (Django)
- **Framework**: Django 6.0.3
- **Database**: SQLite (db.sqlite3)
- **AI Modules**: Loaded from ai_engine/
  - Anomaly Detector (Isolation Forest)
  - Threat Classifier (Random Forest)
- **Additional Modules**: scikit-learn, numpy, joblib

### Frontend (React)
- Located in `Futuristic-Dashboard/client/`
- Built with TypeScript and Vite
- Components use shadcn/ui

## Key Files

```
campusshield/
├── manage.py                 # Django management script
├── campusshield/
│   ├── settings.py          # Django configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI application
├── incidents/
│   ├── models.py            # Database models
│   ├── views.py             # View handlers
│   └── urls.py              # App URLs
├── ai_engine/
│   ├── anomaly_detector.py  # ML anomaly detection
│   └── threat_classifier.py # ML threat classification
└── venv/                     # Virtual environment
```

## Verification Commands

### Check Django Setup
```powershell
python manage.py check
```

### Run Database Migrations
```powershell
python manage.py migrate
```

### Create Superuser (Admin)
```powershell
python manage.py createsuperuser
```

### Access Django Admin
Once logged in as superuser, visit: **http://localhost:8000/admin**

## Common Issues & Fixes

### Issue: "Python not found"
**Solution**: Activate virtual environment first
```powershell
.\venv\Scripts\Activate.ps1
```

### Issue: "Port 8000 already in use"
**Solution**: Use a different port
```powershell
python manage.py runserver 127.0.0.1:8001
```

### Issue: "Module not found" errors
**Solution**: Install dependencies
```powershell
pip install -r requirements.txt
```

### Issue: "DJANGO_SECRET_KEY not set" warning
**Solution**: This is normal in development. For production, set:
```powershell
$env:DJANGO_SECRET_KEY = "your-secret-key-here"
```

## Development Workflow

1. **Make changes** to Python/HTML templates
2. **Django auto-reloads** on file changes
3. **Refresh browser** to see changes
4. **Check terminal** for any error messages

## Stopping the Server

Press **CTRL+C** in the terminal where the server is running.

## Database Reset

To reset the database (delete all data):
```powershell
rm db.sqlite3
python manage.py migrate
```

## Helpful URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000 | Dashboard (requires login) |
| http://localhost:8000/accounts/login/ | Login page |
| http://localhost:8000/incidents/ | Incidents list |
| http://localhost:8000/admin/ | Django admin panel |

## Environment Variables

Set these for customization:

```powershell
# Enable/disable debug mode
$env:DJANGO_DEBUG = 'True'

# Set secret key (for production)
$env:DJANGO_SECRET_KEY = 'your-secret-key'

# Database URL (defaults to SQLite)
$env:DATABASE_URL = 'sqlite:///db.sqlite3'
```

## Next Steps

- [ ] Run `start_server.ps1`
- [ ] Access http://localhost:8000
- [ ] Log in with your credentials
- [ ] Create test incidents
- [ ] Test AI analysis features

---

For more information, see the main [README.md](../../README.md)
