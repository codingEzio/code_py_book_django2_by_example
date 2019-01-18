from django.db import models
from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .fields import OrderField


class Subject(models.Model):
    """
        Hierarchy
            Subject => Course => Module => Content
        
        Note for this model file
            fields :: easy-to-understand        won't be explained
            fields :: been-mentioned-elsewhere  won't be explained twice
    """
    
    title   = models.CharField(max_length=200)
    slug    = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['title', ]
    
    def __str__(self):
        return self.title


class Course(models.Model):
    """
        owner       Who created this course
        subject     Which 'kind' does the course belong to
        
        The `subject` (fk) points to the subject (superclass, sort of).
            Later, the `course` itself will be pointed by `Module` (part).
    """

    # ----- ----- ----- -----
    
    owner       = models.ForeignKey(User,
                                    related_name='courses_created',
                                    on_delete=models.CASCADE)
    subject     = models.ForeignKey(Subject,
                                    related_name='courses',
                                    on_delete=models.CASCADE)
    
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True)
    
    overview    = models.TextField()
    created     = models.DateTimeField(auto_now_add=True)
    
    # ----- ----- ----- -----
    
    students    = models.ManyToManyField(User,
                                         related_name='courses_joined',
                                         blank=True)
    
    class Meta:
        ordering = ['-created', ]
    
    def __str__(self):
        return self.title


class Module(models.Model):
    """
        ( Same thing applies to `Content` )
        
        The newly added `order` means that
            | the order for a new module will be assigned
            | by adding 1 to the last module of the same `Course` object
    """
    
    course      = models.ForeignKey(Course,
                                    related_name='modules',
                                    on_delete=models.CASCADE)
    
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    order       = OrderField(blank=True,
                             for_fields=['course'])

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return '{}. {}'.format(self.order, self.title)
    
    
class Content(models.Model):
    """
        Two parts
            1. A normal foreign-key that pointing to `Module`
            2. A generic foreign-key (for the detailed sub content models)
        
        For the `GenericForeignKey` part
            `ForeignKey`                a fk field to ContentType model
            `PositiveIntegerField`    store the pk of the related object
            `item`                      combine the 2 prev fields (as GFK)
        
        ----- ----- -----
        
        The newly added `limit_choices_to`
            does limit < the objs that can be used for generic relationship >
            the values inside would be the lowercase version of the classnames :D
        
        ----- ----- -----
        
        The newly added `order` means that
            | the order for a new content will be assigned
            | by adding 1 to the last content of the same `Module` object
    """
    
    module          = models.ForeignKey(Module,
                                        related_name='contents',
                                        on_delete=models.CASCADE)
    
    content_type    = models.ForeignKey(ContentType,
                                        on_delete=models.CASCADE,
                                        limit_choices_to={
                                            'model__in': (
                                                'text', 'video',
                                                'image', 'file',
                                            )
                                        })
    
    object_id       = models.PositiveIntegerField()
    item            = GenericForeignKey('content_type', 'object_id')
    
    order           = OrderField(blank=True,
                                 for_fields=['module'])
    
    class Meta:
        ordering = ['order']
    
    
# ---- Content related ----

class ItemBase(models.Model):
    """
        Since this model is an 'abstract' one.
            No table will be created in the database.
    """
    
    owner   = models.ForeignKey(User,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)
    title   = models.CharField(max_length=250)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.title
    

class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file    = models.FileField(upload_to='files')


class Image(ItemBase):
    image   = models.ImageField(upload_to='images')


class Video(ItemBase):
    video   = models.URLField()