#!/bin/bash
# CampusShield AI - Production Deployment Quick Start
# This script helps setup and verify production deployment

set -e  # Exit on first error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║       CampusShield AI - Production Deployment Setup           ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Utility functions
log_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

log_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

log_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Menu
show_menu() {
    echo ""
    echo "What would you like to do?"
    echo "1) Verify production readiness"
    echo "2) Generate SECRET_KEY"
    echo "3) Create .env.production file"
    echo "4) Run security checks"
    echo "5) View deployment guide"
    echo "6) Exit"
    echo ""
}

# 1. Verify readiness
verify_readiness() {
    log_step "Verifying production readiness..."
    
    echo ""
    log_step "Checking Python packages..."
    python -c "import django; print(f'Django: {django.__version__}')" && log_success "Django installed"
    python -c "import rest_framework; print(f'DRF installed')" && log_success "Django REST Framework installed"
    
    echo ""
    log_step "Checking project structure..."
    
    files=(
        "campusshield/manage.py"
        "campusshield/campusshield/settings.py"
        "campusshield/incidents/models.py"
        "campusshield/ai_engine/__init__.py"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            log_success "Found: $file"
        else
            log_error "Missing: $file"
        fi
    done
    
    echo ""
    log_step "Running Django checks..."
    cd campusshield && python manage.py check && log_success "Django checks passed" && cd ..
    
    echo ""
    log_success "Production readiness verified!"
}

# 2. Generate SECRET_KEY
generate_secret_key() {
    log_step "Generating cryptographically secure SECRET_KEY..."
    
    echo ""
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    
    echo ""
    log_success "Generated SECRET_KEY:"
    echo ""
    echo "    $SECRET_KEY"
    echo ""
    log_warning "Copy this key and paste it into your .env.production file as:"
    echo "    DJANGO_SECRET_KEY=$SECRET_KEY"
}

# 3. Create .env.production
create_env_file() {
    log_step "Creating .env.production configuration..."
    
    if [ -f ".env.production" ]; then
        log_warning ".env.production already exists"
        read -p "Overwrite? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return
        fi
    fi
    
    cp .env.production.example .env.production
    log_success "Created .env.production"
    
    echo ""
    log_step "Configuration file created. Please edit the following values:"
    echo ""
    echo "Required settings in .env.production:"
    echo "  1. DJANGO_ENVIRONMENT=production"
    echo "  2. DJANGO_SECRET_KEY=<generated above>"
    echo "  3. ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com"
    echo "  4. DATABASE_URL=postgresql://user:pass@localhost:5432/campusshield"
    echo "  5. DEBUG=False"
    echo ""
    
    if command -v nano &> /dev/null; then
        read -p "Open .env.production in editor? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            nano .env.production
        fi
    fi
}

# 4. Security checks
run_security_checks() {
    log_step "Running comprehensive security checks..."
    
    echo ""
    
    if [ -f "campusshield/security_check.py" ]; then
        cd campusshield && python security_check.py && cd ..
    else
        log_error "security_check.py not found"
    fi
    
    echo ""
    
    if [ -f "generate_deployment_report.py" ]; then
        python generate_deployment_report.py
    else
        log_error "generate_deployment_report.py not found"
    fi
}

# 5. View deployment guide
view_deployment_guide() {
    log_step "Production Deployment Guide"
    echo ""
    echo "For complete deployment instructions, see: PRODUCTION_DEPLOYMENT.md"
    echo ""
    
    if command -v less &> /dev/null; then
        read -p "View PRODUCTION_DEPLOYMENT.md? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            less PRODUCTION_DEPLOYMENT.md
        fi
    fi
}

# Main loop
main() {
    while true; do
        show_menu
        read -p "Enter choice (1-6): " choice
        
        case $choice in
            1) verify_readiness ;;
            2) generate_secret_key ;;
            3) create_env_file ;;
            4) run_security_checks ;;
            5) view_deployment_guide ;;
            6) 
                echo ""
                log_success "Goodbye!"
                exit 0 
                ;;
            *)
                log_error "Invalid choice. Please try again."
                ;;
        esac
    done
}

# Run main
main
