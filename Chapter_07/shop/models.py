from django.db import models
from django.urls import reverse

from parler.models import TranslatableModel, TranslatedFields


class Category(TranslatableModel):
    """
    
    """
    
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, unique=True),
    )
    
    class Meta:
        """
            For those "translated" fields, it can be
                no longer do 'ordering' by override the attrs in class `Meta`.
            
            We'll comment that line for now :D
        """
        
        # ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Product(TranslatableModel):
    """
    
    """
    
    translations = TranslatedFields(
        name=models.CharField(max_length=200, db_index=True),
        slug=models.SlugField(max_length=200, db_index=True),
        description=models.TextField(blank=True),
    )
    
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='products/%Y/%m/%d',
                              blank=True)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    available = models.BooleanField(default=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        """
            Same thing (translated-fields :: can-no-longer-use-ordering)
                applies to this `Product` model (we'll comment this for now)
            
            And the `index_together`.
                It (django-parlor) does not support this right now :D
        """
        
        # ordering = ('name',)
        # index_together = (('id', 'slug'),)
        pass
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])