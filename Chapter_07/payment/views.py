from io import BytesIO

from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

import braintree
import weasyprint

from orders.models import Order


def payment_process(request):
    """
    
    """
    
    # Simply to find/get what we need
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        
        result = braintree.Transaction.sale({
            'amount'              : '{:.2f}'.format(order.get_total_cost()),
            'payment_method_nonce': nonce,
            'options'             : { 'submit_for_settlement': True, }
        })
        
        if result.is_success:
            order.paid = True
            order.braintree_id = result.transaction.id
            
            order.save()
            
            # ----- ----- Start of Send PDF by Email ----- -----
            
            # Part 1 - create email
            subject = 'My Shop - Invoice no. {}'.format(order_id)
            message = 'Please find attached the invoice for ur recent purchase.'
            
            # Do make sure the email here
            #   is the SAME as the one you've conf_ed at the backend!
            email = EmailMessage(subject,
                                 message,
                                 'appleincceo@qq.com',
                                 [order.email])
            
            # Part 2 - generate PDF
            out = BytesIO()
            html = render_to_string('orders/order/pdf.html',
                                    { 'order': order })
            stylesheets = [
                weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')
            ]
            
            weasyprint.HTML(string=html).write_pdf(out,
                                                   stylesheets=stylesheets)
            
            # Part 3 - attach PDf file
            email.attach(
                'order_{}.pdf'.format(order.id),
                out.getvalue(),
                'application/pdf'
            )
            email.send()
            
            # ----- ----- End of Send PDF by Email ----- -----
            
            return redirect('payment:done')
        
        else:
            return redirect('payment:canceled')
    
    else:
        
        client_token = braintree.ClientToken.generate()
        
        return render(request,
                      'payment/process.html', { 'order'       : order,
                                                'client_token': client_token })


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