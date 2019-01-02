from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from shop.models import Product

from .cart import Cart
from .forms import CartAddProductForm

from coupons.forms import CouponApplyForm


@require_POST
def cart_add(request, product_id):
    """
        ---- Lemme break down this function ----

        <cart, product>
            Init a new cart inst 
            Query the product u added (by ID)

        <form, cleaned>
            Init a 'cardAdd' form ('POST')

        <card.add>
            Submit with 'product, quantity' and 'update-or-add'    
    """
    
    cart = Cart(request)
    
    product = get_object_or_404(Product, id=product_id)
    
    form = CartAddProductForm(request.POST)
    
    if form.is_valid():
        input_data = form.cleaned_data
        
        cart.add(product=product,
                 quantity=input_data['quantity'],
                 update_quantity=input_data['update'])
    
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    """
    
    """
    
    cart = Cart(request)
    
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product)
    
    return redirect('cart:cart_detail')


def cart_detail(request):
    """
    
    """
    
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'update'  : True
            }
        )
    
    coupon_apply_form = CouponApplyForm()
    
    return render(request,
                  'cart/detail.html', { 'cart'             : cart,
                                        'coupon_apply_form': coupon_apply_form })