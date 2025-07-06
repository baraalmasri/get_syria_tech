import stripe
import json
from decimal import Decimal
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.urls import reverse
from cart.cart import Cart
from orders.models import Order, OrderItem
from shop.models import Product

# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def checkout(request):
    """Display checkout page with order summary"""
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('shop:product_list')
    
    # Calculate total
    total_amount = cart.get_total_price()
    
    context = {
        'cart': cart,
        'total_amount': total_amount,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
    }
    
    return render(request, 'payments/checkout.html', context)

@login_required
@require_POST
def create_payment_intent(request):
    """Create Stripe Payment Intent"""
    try:
        cart = Cart(request)
        
        if len(cart) == 0:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Calculate total amount in cents
        total_amount = int(cart.get_total_price() * 100)
        
        # Create Payment Intent
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency=settings.DEFAULT_CURRENCY.lower(),
            metadata={
                'user_id': request.user.id,
                'cart_items': json.dumps([
                    {
                        'product_id': item['product'].id,
                        'quantity': item['quantity'],
                        'price': str(item['price'])
                    }
                    for item in cart
                ])
            }
        )
        
        return JsonResponse({
            'client_secret': intent.client_secret,
            'amount': total_amount
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def payment_success(request):
    """Handle successful payment"""
    payment_intent_id = request.GET.get('payment_intent')
    
    if not payment_intent_id:
        messages.error(request, 'Payment information not found.')
        return redirect('shop:product_list')
    
    try:
        # Retrieve payment intent from Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status == 'succeeded':
            # Create order from cart
            cart = Cart(request)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                address=request.user.userprofile.address or '',
                postal_code=request.user.userprofile.postal_code or '',
                city=request.user.userprofile.city or '',
                paid=True,
                stripe_payment_intent_id=payment_intent_id
            )
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear cart
            cart.clear()
            
            messages.success(request, f'Your order #{order.id} has been placed successfully!')
            return render(request, 'payments/payment_success.html', {'order': order})
        
        else:
            messages.error(request, 'Payment was not successful.')
            return redirect('payments:checkout')
            
    except Exception as e:
        messages.error(request, f'Error processing payment: {str(e)}')
        return redirect('payments:checkout')

@login_required
def payment_cancelled(request):
    """Handle cancelled payment"""
    messages.info(request, 'Payment was cancelled.')
    return render(request, 'payments/payment_cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        # Handle successful payment
        print(f"Payment succeeded: {payment_intent['id']}")
        
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        # Handle failed payment
        print(f"Payment failed: {payment_intent['id']}")
        
    else:
        print(f"Unhandled event type: {event['type']}")
    
    return HttpResponse(status=200)

