from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # Filter by category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Filter by brand
    brand = request.GET.get('brand')
    if brand:
        products = products.filter(compatible_brand=brand)
    
    # Sorting
    sort_by = request.GET.get('sort')
    if sort_by:
        if sort_by in ['name', '-name', 'price', '-price', '-created']:
            products = products.order_by(sort_by)
    else:
        products = products.order_by('name')
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    
    # Get related products from the same category
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'shop/product_detail.html', context)

