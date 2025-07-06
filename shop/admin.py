from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'category', 'compatible_brand', 'product_type', 
                   'price', 'stock_quantity', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category', 'compatible_brand', 'product_type']
    list_editable = ['price', 'available', 'stock_quantity']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'image')
        }),
        ('Product Details', {
            'fields': ('compatible_brand', 'product_type', 'color', 'material')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity', 'available')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')

