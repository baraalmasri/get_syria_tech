# From Syria - Phone Accessories E-commerce Platform

A modern Django-based e-commerce platform for selling phone accessories and covers, featuring user authentication, shopping cart functionality, Stripe payment integration, and a responsive design.

## 🚀 Features

- **Modern E-commerce Platform**: Complete online store for phone accessories
- **User Authentication**: Registration, login, profile management
- **Shopping Cart**: Session-based cart with add/remove functionality
- **Stripe Integration**: Secure payment processing
- **Admin Interface**: Beautiful Unfold admin theme
- **Responsive Design**: Mobile-first design with Tailwind CSS
- **Product Management**: Categories, products, inventory tracking
- **Order Management**: Complete order processing workflow
- **Security**: Production-ready security configurations

## 🛠 Technology Stack

- **Backend**: Django 5.2.4, Python 3.11
- **Database**: PostgreSQL (production), SQLite (development)
- **Cache**: Redis
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Payment**: Stripe API
- **Server**: Gunicorn + Nginx
- **Deployment**: Digital Ocean + Let's Encrypt SSL

## 📁 Project Structure

```
phone_shop/
├── phone_shop/           # Main project directory
│   ├── settings.py       # Development settings
│   ├── settings_production.py  # Production settings
│   ├── urls.py          # URL configuration
│   └── wsgi.py          # WSGI configuration
├── shop/                # Product catalog app
├── cart/                # Shopping cart app
├── orders/              # Order management app
├── users/               # User authentication app
├── payments/            # Stripe payment integration
├── templates/           # HTML templates
├── static/              # Static files (CSS, JS, images)
├── media/               # User uploaded files
├── deployment/          # Deployment configurations
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── manage.py           # Django management script
```

## 🚀 Quick Start (Development)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd phone_shop
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Load sample data**
   ```bash
   python manage.py populate_data
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Website: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 🌐 Production Deployment

For production deployment on Digital Ocean with the fromsyria.tech domain, follow the comprehensive deployment guide:

**[📖 Complete Deployment Guide](DEPLOYMENT_GUIDE.md)**

### Quick Deployment Steps

1. **Set up Digital Ocean droplet** (Ubuntu 22.04 LTS, 2GB+ RAM)
2. **Configure domain DNS** (fromsyria.tech → server IP)
3. **Run deployment script**:
   ```bash
   chmod +x deployment/deploy.sh
   ./deployment/deploy.sh
   ```
4. **Configure environment variables** in `.env`
5. **Set up SSL certificates** with Let's Encrypt
6. **Configure Stripe** with live API keys

## 🔧 Configuration

### Environment Variables

Key environment variables (see `.env.example` for complete list):

```env
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOST=fromsyria.tech
DB_NAME=phone_shop_db
DB_USER=phone_shop_user
DB_PASSWORD=your-password
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
```

### Stripe Configuration

1. Create Stripe account at https://stripe.com
2. Get API keys from Stripe Dashboard
3. Configure webhook endpoints for payment processing
4. Update environment variables with live keys

## 📱 Admin Interface

Access the admin interface at `/admin/` with superuser credentials:

- **Products**: Manage product catalog
- **Categories**: Organize products
- **Orders**: View and manage customer orders
- **Users**: Manage customer accounts
- **Unfold Theme**: Modern, responsive admin interface

## 🛒 E-commerce Features

### Product Management
- Product categories and subcategories
- Product images and descriptions
- Inventory tracking
- Price management

### Shopping Cart
- Session-based cart (no login required)
- Add/remove products
- Quantity management
- Cart persistence

### User Accounts
- User registration and login
- Profile management
- Order history
- Address management

### Payment Processing
- Stripe integration
- Secure payment forms
- Order confirmation
- Payment status tracking

## 🔒 Security Features

- HTTPS/SSL encryption
- CSRF protection
- Secure headers
- Input validation
- Session security
- Rate limiting
- SQL injection protection

## 📊 Performance Features

- Redis caching
- Static file optimization
- Database query optimization
- Gzip compression
- CDN-ready static files

## 🚀 Deployment Files

The `deployment/` directory contains all necessary files for production deployment:

- `deploy.sh` - Automated deployment script
- `update.sh` - Application update script
- `nginx_phone_shop.conf` - Nginx configuration
- `phone_shop.service` - Systemd service file
- `gunicorn.conf.py` - Gunicorn configuration

## 📝 Management Commands

Custom Django management commands:

```bash
# Populate database with sample data
python manage.py populate_data

# Collect static files for production
python manage.py collectstatic

# Create database backup
python manage.py dbbackup

# Health check
curl http://localhost:8000/health/
```

## 🐛 Troubleshooting

Common issues and solutions:

1. **Database connection errors**: Check PostgreSQL service and credentials
2. **Static files not loading**: Run `collectstatic` and check Nginx config
3. **Payment processing issues**: Verify Stripe API keys and webhook setup
4. **SSL certificate problems**: Check domain DNS and Let's Encrypt setup

For detailed troubleshooting, see the [Deployment Guide](DEPLOYMENT_GUIDE.md).

## 📞 Support

- **Documentation**: See `DEPLOYMENT_GUIDE.md` for comprehensive setup instructions
- **Issues**: Check logs in `/var/log/` for error details
- **Monitoring**: Use `/health/` endpoint for system status

## 📄 License

This project is created for From Syria (fromsyria.tech) phone accessories business.

## 🎯 Next Steps

After deployment:

1. **Add Products**: Use admin interface to add your phone accessories
2. **Configure Stripe**: Set up live payment processing
3. **Test Orders**: Process test orders to verify functionality
4. **Monitor Performance**: Set up monitoring and alerts
5. **Marketing**: Configure SEO and analytics

---

**Ready to deploy?** Follow the [Complete Deployment Guide](DEPLOYMENT_GUIDE.md) for step-by-step instructions.

