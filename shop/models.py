from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    PHONE_BRANDS = [
        ('apple', 'Apple iPhone'),
        ('samsung', 'Samsung Galaxy'),
        ('huawei', 'Huawei'),
        ('xiaomi', 'Xiaomi'),
        ('oppo', 'OPPO'),
        ('vivo', 'Vivo'),
        ('oneplus', 'OnePlus'),
        ('google', 'Google Pixel'),
        ('sony', 'Sony Xperia'),
        ('lg', 'LG'),
        ('nokia', 'Nokia'),
        ('motorola', 'Motorola'),
        ('universal', 'Universal'),
    ]
    
    PRODUCT_TYPES = [
        ('case', 'Phone Case'),
        ('cover', 'Phone Cover'),
        ('screen_protector', 'Screen Protector'),
        ('charger', 'Charger'),
        ('cable', 'Cable'),
        ('power_bank', 'Power Bank'),
        ('headphones', 'Headphones'),
        ('car_mount', 'Car Mount'),
        ('wireless_charger', 'Wireless Charger'),
        ('pop_socket', 'Pop Socket'),
        ('ring_holder', 'Ring Holder'),
        ('wallet_case', 'Wallet Case'),
    ]
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Phone accessories specific fields
    compatible_brand = models.CharField(max_length=20, choices=PHONE_BRANDS, default='universal')
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='case')
    color = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=100, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # SEO fields
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0 and self.available

