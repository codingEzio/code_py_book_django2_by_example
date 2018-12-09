from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class PublishedManager(models.Manager):
    """
        This class is for customizing our own "manager" :P
        
        For the methods down below,
            we're overriding it to include our own filter in the result.
            
        There're three things happened
            1. Inherit the 'Manager' superclass (got its methods)
            2. Rewriting method (then we got a customized result set)
            3. Ready for use (Post.XX.all() depends on a variable name))
            
        Lastly, for the commands I skipped,
        #TODO
            Type it, test it, understand it, then *taking notes* in '02_queryset.md'.
            These 3 lines should be deleted after the notes were taken :P
    """
    
    def get_queryset(self):
        return super(PublishedManager, self) \
            .get_queryset() \
            .filter(status='draft')


class Post(models.Model):
    """
        Trans to DB
            CharField   VARCHAR
            TextField   TEXT
        
        SlugField
            A short label for sth, used in URLs, [a-zA-Z_-] only
            It's possible that multiple posts got same slug,
                so it's better add a 'unique' factor, e.g. a date'd be nice
            
            e.g.
                stackoverflow.com/.../what-is-a-slug-in-django
        
        ForeignKey
            The params (of var 'author') are related to this (fk).
            
            on_delete=models.CASCADE
                for our cases, it's <one-author> TO <many-posts>
                so when a user is deleted => his/her posts were deleted as well
            
            related_name
                quote: "easily access the related objects"
                
                the value "blog_posts"
                    blog    app name
                    posts   table name (same as class's name in models.py)
                    
            One more words,
                you CAN override the default primary key (aka ID)
                just add `primary_key=True` to one of ur model fields.
                
        The three time-related params
            timezone.now    timezone-aware version of 'datetime.now'
            auto_now_add    auto add the time when the object is created
            auto_now        the last time the obj was updated (update when saving)
        
        choices
            The '__Field' is just widgets of HTML,
            so the "choices" might be the vals of 'select/option' in HTML.
    """
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    
    objects = models.Manager()
    
    # TABLE_AND_ALSO_MODEL_NAME
    #   .VARIABLE   (i.e. published)
    #   .METHOD     (e.g. all() )
    published = PublishedManager()
    
    class Meta:
        """
            Quote
                "Give your model metadata by using an inner 'Meta' class"
            
            What variables can be used?
                Go check the doc of 'django.db.models.Options'.
                This inner class could do a large influences in the 'param' part.
            
            The val ('-publish') means
                ordering by 'publish' by DESC (there's also publish, ?publish)
        """
        
        ordering = ('-publish',)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        """ Generating nice (& SEO-friendly) urls (directly related to 'urls.py')
        """
        
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])