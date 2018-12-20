from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class Profile(models.Model):
    """
    
    """
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)


class Contact(models.Model):
    """
        This model is for the feature 'follower system' :D
            and it won't be displayed at the very frontend (it'll, but deeper)
            
        The base model is still 'User' (provided by Django)
            we're just creating other stuff attaching to it :D
            
        Plain words for code down below
            1. The user
            2. The user being followed
            3. The time of user being followed
        
        Oh, lemme repeat it again
            The index was auto created since it's a "ForeignKey"
    """
    
    user_from = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User',
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add=True,
                                   db_index=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return '{} follows {}'.format(self.user_from,
                                      self.user_to)


# Another way of adding fields (to models)
#   through         Many-to-many specific
#   symmetrical     I don't (auto) follow u if you've followed me
User.add_to_class('following',
                  models.ManyToManyField('self',
                                         through=Contact,
                                         related_name='followers',
                                         symmetrical=False))