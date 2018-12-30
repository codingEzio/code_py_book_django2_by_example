from django.shortcuts import render, get_object_or_404, redirect

import braintree

from orders.models import Order


def payment_done(request):
    """
    
    """
    
    return render(request,
                  'payment/done.html')


def payment_canceled(request):
    """
    
    """
    
    return render(request,
                  'payment/canceled.html')