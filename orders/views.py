from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def order_create(request):
    return HttpResponse("Order create view - coming soon!")

def payment_process(request):
    return HttpResponse("Payment process view - coming soon!")

def payment_done(request):
    return HttpResponse("Payment done view - coming soon!")

def payment_canceled(request):
    return HttpResponse("Payment canceled view - coming soon!")

@csrf_exempt
@require_POST
def stripe_webhook(request):
    return HttpResponse("Stripe webhook - coming soon!")

