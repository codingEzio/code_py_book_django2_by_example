from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Order, OrderItem
from .forms import OrderCreateForm

# Don't use `.tasks` in here
#   Celery does NOT recognize the relative path,
#   the one we're using is letting Celery treating it as "package".
from orders.tasks import order_created

from cart.cart import Cart

import weasyprint


def order_create(request):
    """
    
    """
    
    cart = Cart(request)
    
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():
            order = form.save(commit=False)

            # the last attr are fields in each databases
            #   so we're just trying to assign store 'fields' :D
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
                
            order.save()
            
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


@staff_member_required
def admin_order_pdf(request, order_id):
    """
        1. Get data (and templates for displaying data)
        2. Set type (cuz you'll need to download it, right?)
        3. Using the module (configuring stuff, e.g. the CSS :P)
    """
    
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            { 'order': order })
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'filename=order_{}.pdf'.format(order.id)
    )
    
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[
            weasyprint.CSS(
                settings.STATIC_ROOT + 'css/pdf.css'
            )
        ]
    )
    
    return response