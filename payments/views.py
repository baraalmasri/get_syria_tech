from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from cart.cart import Cart
from orders.models import Order
from .utils import generate_payeer_url
from django.conf import settings

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('shop:product_list')
    
    total_amount = cart.get_total_price()
    
    # Create a preliminary order
    order = Order.objects.create(
        user=request.user,
        paid=False  # Mark as not paid initially
    )
    
    payeer_url = generate_payeer_url(
        merchant_id=settings.PAYEER_MERCHANT_ID,
        secret_key=settings.PAYEER_SECRET_KEY,
        amount=total_amount,
        order_id=order.id,
        currency='USD',
        description=f'Order #{order.id}'
    )

    # Clear the cart before redirecting
    cart.clear()

    return redirect(payeer_url)

@login_required
def payment_success(request):
    order_id = request.GET.get('m_orderid')
    
    if not order_id:
        messages.error(request, 'Payment information not found.')
        return redirect('shop:product_list')
    
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.paid = True
    order.save()

    messages.success(request, f'Your order #{order.id} has been placed successfully!')
    return render(request, 'payments/payment_success.html', {'order': order})

@login_required
def payment_cancelled(request):
    messages.info(request, 'Payment was cancelled.')
    return render(request, 'payments/payment_cancelled.html')
