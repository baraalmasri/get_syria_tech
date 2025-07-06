from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('success/', views.payment_success, name='payment_success'),
    path('cancelled/', views.payment_cancelled, name='payment_cancelled'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]

