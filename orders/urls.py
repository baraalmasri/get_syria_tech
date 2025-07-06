from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/', views.payment_process, name='payment_process'),
    path('payment/done/', views.payment_done, name='payment_done'),
    path('payment/canceled/', views.payment_canceled, name='payment_canceled'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]

