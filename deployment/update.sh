#!/bin/bash

# Phone Shop Update Script
# Use this script to update the application after initial deployment

set -e

PROJECT_DIR="/var/www/phone_shop"
GREEN='\033[0;32m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_status "🔄 Updating Phone Shop application..."

cd $PROJECT_DIR

print_status "Pulling latest changes from repository..."
git pull origin main

print_status "Activating virtual environment..."
source venv/bin/activate

print_status "Installing/updating dependencies..."
pip install -r requirements.txt

print_status "Collecting static files..."
export DJANGO_SETTINGS_MODULE=phone_shop.settings_production
python manage.py collectstatic --noinput

print_status "Running database migrations..."
python manage.py migrate

print_status "Restarting application..."
sudo systemctl restart phone_shop

print_status "Reloading Nginx..."
sudo systemctl reload nginx

print_status "✅ Update completed successfully!"
print_status "Application is now running the latest version."

