from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    """
        A reminder of some attrs
        
            user
                ForeignKey      1 to many
                on_delete       if the user was del_ed -> all related were del_ed as well
            created
                auto_now_add    the time it was created
                
            ManyToManyField
                For sth like '[users_like_for_img]  <->  [Image] & [User]'
                
                you could retrieve the data like this
                    =>  Image.user_likes.all()  --  how many likes for the img
                    =>  User.image_likes.all()  --  what imgs does the user liked
                
        About the 'index'
            1. it could boost query performance
            2. there's some cases the index would be created automatically
                - fields `ForeignKey`
                - fields with a `unique=True` etc.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    
    created = models.DateField(auto_now_add=True, db_index=True)
    
    users_like_for_img = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                                related_name='images_liked',
                                                blank=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
            Now we're overriding the `save()` method
                in order to "automatically gen the 'slug' field" (based on 'title')
        """
        
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Image, self).save(*args, **kwargs)