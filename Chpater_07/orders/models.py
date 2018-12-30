from django.db import models

from shop.models import Product


class Order(models.Model):
    """
        Store the order details :D
    """
    
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    paid = models.BooleanField(default=False)
    
    # Payment-gateway stuff
    braintree_id = models.CharField(max_length=150,
                                    blank=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_total_cost(self):
        return sum(
            item.get_cost()
            for item in self.items.all()
        )


class OrderItem(models.Model):
    """
        Store items bought (price, quantity)
    """
    
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return '{}'.format(self.id)
    
    def get_cost(self):
        return self.price * self.quantity