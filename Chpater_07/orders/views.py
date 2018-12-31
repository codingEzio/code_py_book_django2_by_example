from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order, OrderItem
from .forms import OrderCreateForm

# Don't use `.tasks` in here
#   Celery does NOT recognize the rel path, the one we're using is "package".
from orders.tasks import order_created

from cart.cart import Cart


def order_create(request):
    """
    
    """
    
    cart = Cart(request)
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            order = form.save()
            
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                
                cart.clear()
                
                # The docs says this
                #   "Apply tasks asynchronously by sending a message."
                order_created.delay(order.id)
                
                # Hmm, interesting
                request.session['order_id'] = order.id
                
                # The old is just rendering a (fake, sort-of) page
                return redirect(reverse('payment:process'))
    
    else:
        form = OrderCreateForm()
    
    return render(request,
                  'orders/order/create.html', { 'cart': cart,
                                                'form': form })


@staff_member_required
def admin_order_detail(request, order_id):
    """
    
    """
    
    order = get_object_or_404(Order, id=order_id)
    
    return render(request,
                  'admin/orders/order/detail.html', { 'order': order })