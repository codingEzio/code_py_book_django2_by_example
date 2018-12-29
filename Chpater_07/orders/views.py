from django.shortcuts import render

from .models import OrderItem
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
                
                return render(request,
                              'orders/order/created.html', { 'order': order })
    else:
        form = OrderCreateForm()
    
    return render(request,
                  'orders/order/create.html', { 'cart': cart,
                                                'form': form })