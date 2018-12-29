from celery import task
from django.core.mail import send_mail

from .models import Order


@task
def order_created(order_id):
    """
    
    """
    
    order = Order.objects.get(id=order_id)
    
    subject = 'Order nr. {}'.format(order.id)
    message = (
        "Hi, {}!\n\n"
        "You've successfully placed an order 😊 .\n"
        "Your order ID is {}".format(
            order.first_name,
            order.id
        )
    )
    
    mail_sent = send_mail(subject,
                          message,
                          "a@a.com",
                          [order.email])
    return mail_sent