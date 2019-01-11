from django.db import models
from django.contrib.auth.models import User


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
    
    class Meta:
        ordering = ['-created', ]
    
    def __str__(self):
        return self.title


class Module(models.Model):
    """
    
    """
    
    course      = models.ForeignKey(Course,
                                    related_name='modules',
                                    on_delete=models.CASCADE)
    
    title       = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.title