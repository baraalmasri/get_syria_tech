from django.core.management.base import BaseCommand
from shop.models import Category, Product

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating categories...')
        
        # Create categories
        categories_data = [
            {'name': 'Phone Cases', 'slug': 'phone-cases'},
            {'name': 'Screen Protectors', 'slug': 'screen-protectors'},
            {'name': 'Chargers & Cables', 'slug': 'chargers-cables'},
            {'name': 'Power Banks', 'slug': 'power-banks'},
            {'name': 'Headphones & Audio', 'slug': 'headphones-audio'},
            {'name': 'Car Accessories', 'slug': 'car-accessories'},
            {'name': 'Wireless Chargers', 'slug': 'wireless-chargers'},
            {'name': 'Phone Holders & Stands', 'slug': 'phone-holders-stands'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'slug': cat_data['slug']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        self.stdout.write('Creating products...')
        
        # Get categories
        cases_cat = Category.objects.get(name='Phone Cases')
        screen_cat = Category.objects.get(name='Screen Protectors')
        chargers_cat = Category.objects.get(name='Chargers & Cables')
        powerbank_cat = Category.objects.get(name='Power Banks')
        audio_cat = Category.objects.get(name='Headphones & Audio')
        car_cat = Category.objects.get(name='Car Accessories')
        wireless_cat = Category.objects.get(name='Wireless Chargers')
        holders_cat = Category.objects.get(name='Phone Holders & Stands')
        
        # Create products
        products_data = [
            # Phone Cases
            {
                'name': 'iPhone 15 Pro Clear Case',
                'category': cases_cat,
                'price': 29.99,
                'description': 'Crystal clear protective case for iPhone 15 Pro with shock absorption.',
                'compatible_brand': 'apple',
                'product_type': 'case',
                'color': 'Clear',
                'material': 'TPU',
                'stock_quantity': 50,
            },
            {
                'name': 'Samsung Galaxy S24 Leather Wallet Case',
                'category': cases_cat,
                'price': 45.99,
                'description': 'Premium leather wallet case with card slots for Samsung Galaxy S24.',
                'compatible_brand': 'samsung',
                'product_type': 'wallet_case',
                'color': 'Black',
                'material': 'Genuine Leather',
                'stock_quantity': 30,
            },
            {
                'name': 'Universal Silicone Phone Case',
                'category': cases_cat,
                'price': 15.99,
                'description': 'Flexible silicone case compatible with most phone sizes.',
                'compatible_brand': 'universal',
                'product_type': 'case',
                'color': 'Blue',
                'material': 'Silicone',
                'stock_quantity': 100,
            },
            
            # Screen Protectors
            {
                'name': 'iPhone 15 Tempered Glass Screen Protector',
                'category': screen_cat,
                'price': 12.99,
                'description': '9H hardness tempered glass screen protector for iPhone 15.',
                'compatible_brand': 'apple',
                'product_type': 'screen_protector',
                'color': 'Clear',
                'material': 'Tempered Glass',
                'stock_quantity': 75,
            },
            {
                'name': 'Samsung Galaxy S24 Privacy Screen Protector',
                'category': screen_cat,
                'price': 18.99,
                'description': 'Privacy screen protector that blocks side viewing for Galaxy S24.',
                'compatible_brand': 'samsung',
                'product_type': 'screen_protector',
                'color': 'Clear',
                'material': 'Tempered Glass',
                'stock_quantity': 40,
            },
            
            # Chargers & Cables
            {
                'name': 'USB-C Fast Charging Cable 6ft',
                'category': chargers_cat,
                'price': 19.99,
                'description': 'High-speed USB-C charging cable with braided design.',
                'compatible_brand': 'universal',
                'product_type': 'cable',
                'color': 'Black',
                'material': 'Braided Nylon',
                'stock_quantity': 80,
            },
            {
                'name': 'Lightning to USB-A Cable 3ft',
                'category': chargers_cat,
                'price': 24.99,
                'description': 'MFi certified Lightning cable for iPhone and iPad.',
                'compatible_brand': 'apple',
                'product_type': 'cable',
                'color': 'White',
                'material': 'TPE',
                'stock_quantity': 60,
            },
            {
                'name': '65W GaN Fast Charger',
                'category': chargers_cat,
                'price': 39.99,
                'description': 'Compact 65W GaN charger with multiple ports.',
                'compatible_brand': 'universal',
                'product_type': 'charger',
                'color': 'White',
                'material': 'Plastic',
                'stock_quantity': 35,
            },
            
            # Power Banks
            {
                'name': '10000mAh Portable Power Bank',
                'category': powerbank_cat,
                'price': 34.99,
                'description': 'Slim 10000mAh power bank with dual USB ports.',
                'compatible_brand': 'universal',
                'product_type': 'power_bank',
                'color': 'Black',
                'material': 'Aluminum',
                'stock_quantity': 45,
            },
            {
                'name': '20000mAh Wireless Power Bank',
                'category': powerbank_cat,
                'price': 59.99,
                'description': 'High-capacity power bank with wireless charging capability.',
                'compatible_brand': 'universal',
                'product_type': 'power_bank',
                'color': 'Blue',
                'material': 'Plastic',
                'stock_quantity': 25,
            },
            
            # Wireless Chargers
            {
                'name': '15W Fast Wireless Charger Pad',
                'category': wireless_cat,
                'price': 29.99,
                'description': 'Fast 15W wireless charging pad with LED indicator.',
                'compatible_brand': 'universal',
                'product_type': 'wireless_charger',
                'color': 'Black',
                'material': 'Plastic',
                'stock_quantity': 40,
            },
            {
                'name': 'MagSafe Compatible Wireless Charger',
                'category': wireless_cat,
                'price': 49.99,
                'description': 'MagSafe compatible wireless charger for iPhone 12 and newer.',
                'compatible_brand': 'apple',
                'product_type': 'wireless_charger',
                'color': 'White',
                'material': 'Aluminum',
                'stock_quantity': 30,
            },
            
            # Phone Holders
            {
                'name': 'Adjustable Phone Ring Holder',
                'category': holders_cat,
                'price': 9.99,
                'description': '360-degree rotating phone ring holder and stand.',
                'compatible_brand': 'universal',
                'product_type': 'ring_holder',
                'color': 'Silver',
                'material': 'Metal',
                'stock_quantity': 90,
            },
            {
                'name': 'PopSocket Grip and Stand',
                'category': holders_cat,
                'price': 14.99,
                'description': 'Collapsible grip and stand for phones and tablets.',
                'compatible_brand': 'universal',
                'product_type': 'pop_socket',
                'color': 'Blue',
                'material': 'Plastic',
                'stock_quantity': 70,
            },
            
            # Car Accessories
            {
                'name': 'Magnetic Car Phone Mount',
                'category': car_cat,
                'price': 24.99,
                'description': 'Strong magnetic car mount for dashboard or windshield.',
                'compatible_brand': 'universal',
                'product_type': 'car_mount',
                'color': 'Black',
                'material': 'Plastic',
                'stock_quantity': 55,
            },
        ]
        
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

