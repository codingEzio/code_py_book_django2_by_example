from django.db import models
from django.core.validators import (MinValueValidator,
                                    MaxValueValidator)


class Coupon(models.Model):
    """
    
    """
    
    # the code for discount XD
    code = models.CharField(max_length=50,
                            unique=True)
    
    # the time that indicates whether it's valid or not
    #   e.g. From <Dec.01> To <Dec.31>
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    
    # percentage to the price
    discount = models.IntegerField(validators=[MinValueValidator,
                                               MaxValueValidator])
    
    # simply you could use it or not
    active = models.BooleanField()
    
    def __str__(self):
        return self.code