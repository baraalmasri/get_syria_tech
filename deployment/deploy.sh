#!/bin/bash

# Phone Shop Django Application Deployment Script
# Run this script on your Digital Ocean server

set -e  # Exit on any error

echo "🚀 Starting Phone Shop deployment..."

# Configuration
PROJECT_NAME="phone_shop"
PROJECT_DIR="/var/www/$PROJECT_NAME"
REPO_URL="https://github.com/yourusername/phone_shop.git"  # Update with your repo
PYTHON_VERSION="3.11"
DB_NAME="phone_shop_db"
DB_USER="phone_shop_user"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

print_status "Installing required system packages..."
sudo apt install -y python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx redis-server \
    git curl wget unzip supervisor \
    build-essential libpq-dev libjpeg-dev libpng-dev \
    certbot python3-certbot-nginx

print_status "Setting up PostgreSQL database..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;" || true
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD 'secure_password_123';" || true
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';" || true
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';" || true
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';" || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" || true

print_status "Creating project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

print_status "Cloning project repository..."
if [ -d "$PROJECT_DIR/.git" ]; then
    cd $PROJECT_DIR
    git pull origin main
else
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

print_status "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

print_status "Creating necessary directories..."
mkdir -p logs media staticfiles
sudo mkdir -p /var/log/gunicorn
sudo chown $USER:$USER /var/log/gunicorn

print_status "Setting up environment variables..."
if [ ! -f .env ]; then
    cp .env.example .env
    print_warning "Please edit .env file with your production settings"
    print_warning "Especially: SECRET_KEY, DB_PASSWORD, STRIPE_KEYS"
fi

print_status "Running Django migrations..."
export DJANGO_SETTINGS_MODULE=phone_shop.settings_production
python manage.py collectstatic --noinput
python manage.py migrate

print_status "Creating Django superuser..."
echo "Please create a superuser for Django admin:"
python manage.py createsuperuser

print_status "Setting up systemd service..."
sudo cp deployment/phone_shop.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable phone_shop
sudo systemctl start phone_shop

print_status "Setting up Nginx..."
sudo cp deployment/nginx_phone_shop.conf /etc/nginx/sites-available/phone_shop
sudo ln -sf /etc/nginx/sites-available/phone_shop /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

print_status "Setting up SSL certificate..."
sudo certbot --nginx -d fromsyria.tech -d www.fromsyria.tech

print_status "Setting up firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

print_status "Setting up log rotation..."
sudo tee /etc/logrotate.d/phone_shop > /dev/null <<EOF
/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
    postrotate
        systemctl reload phone_shop
    endscript
}
EOF

print_status "Setting correct permissions..."
sudo chown -R $USER:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR
sudo chmod -R 775 $PROJECT_DIR/media
sudo chmod -R 775 $PROJECT_DIR/logs

print_status "Restarting services..."
sudo systemctl restart phone_shop
sudo systemctl restart nginx

print_status "Deployment completed successfully! 🎉"
print_status "Your website should now be available at: https://fromsyria.tech"
print_status ""
print_status "Next steps:"
print_status "1. Edit .env file with your production settings"
print_status "2. Update Stripe keys for live payments"
print_status "3. Configure email settings"
print_status "4. Add your products through Django admin"
print_status ""
print_status "Useful commands:"
print_status "- Check service status: sudo systemctl status phone_shop"
print_status "- View logs: sudo journalctl -u phone_shop -f"
print_status "- Restart application: sudo systemctl restart phone_shop"
print_status "- Django admin: https://fromsyria.tech/admin/"

