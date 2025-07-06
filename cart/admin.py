from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Cart, CartItem

class CartItemInline(TabularInline):
    model = CartItem
    extra = 0
    raw_id_fields = ['product']

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'get_total_items', 'get_total_price', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['user__username', 'session_key']
    inlines = [CartItemInline]
    list_per_page = 20
    
    def get_total_items(self, obj):
        return obj.get_total_items()
    get_total_items.short_description = 'Total Items'
    
    def get_total_price(self, obj):
        return f'${obj.get_total_price():.2f}'
    get_total_price.short_description = 'Total Price'

@admin.register(CartItem)
class CartItemAdmin(ModelAdmin):
    list_display = ['id', 'cart', 'product', 'quantity', 'get_total_price', 'created']
    list_filter = ['created', 'updated']
    search_fields = ['product__name', 'cart__user__username']
    raw_id_fields = ['cart', 'product']
    
    def get_total_price(self, obj):
        return f'${obj.get_total_price():.2f}'
    get_total_price.short_description = 'Total Price'

