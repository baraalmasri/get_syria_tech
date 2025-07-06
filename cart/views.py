from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from shop.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    
    context = {
        'cart': cart,
    }
    
    return render(request, 'cart/cart_detail.html', context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    override_quantity = request.POST.get('override', False)
    
    # Check if product is available and in stock
    if not product.available or product.stock_quantity < quantity:
        messages.error(request, f'Sorry, {product.name} is not available in the requested quantity.')
        return redirect('shop:product_detail', id=product.id, slug=product.slug)
    
    cart.add(product=product, quantity=quantity, override_quantity=override_quantity)
    messages.success(request, f'{product.name} has been added to your cart.')
    
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'{product.name} has been removed from your cart.')
    
    return redirect('cart:cart_detail')

@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        if product.stock_quantity >= quantity:
            cart.add(product=product, quantity=quantity, override_quantity=True)
            messages.success(request, f'Cart updated successfully.')
        else:
            messages.error(request, f'Sorry, only {product.stock_quantity} items available.')
    else:
        cart.remove(product)
        messages.success(request, f'{product.name} has been removed from your cart.')
    
    return redirect('cart:cart_detail')

