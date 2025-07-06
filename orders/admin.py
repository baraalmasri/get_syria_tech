from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Order, OrderItem

class OrderItemInline(TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'status', 
                   'payment_status', 'paid', 'created', 'updated', 'total_amount']
    list_filter = ['paid', 'status', 'payment_status', 'created', 'updated']
    inlines = [OrderItemInline]
    search_fields = ['first_name', 'last_name', 'email', 'id']
    list_editable = ['status', 'payment_status']
    list_per_page = 20
    
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'payment_status', 'paid')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'postal_code', 'city', 'country')
        }),
        ('Payment Information', {
            'fields': ('stripe_payment_intent_id', 'stripe_checkout_session_id')
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('tracking_number', 'shipping_carrier'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['stripe_payment_intent_id', 'stripe_checkout_session_id']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')

@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity', 'get_cost']
    list_filter = ['order__created']
    search_fields = ['order__id', 'product__name']
    raw_id_fields = ['order', 'product']
    
    def get_cost(self, obj):
        return obj.get_cost()
    get_cost.short_description = 'Total Cost'

