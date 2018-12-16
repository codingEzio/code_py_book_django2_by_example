from django import forms
from .models import Image

from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    """
    
    """
    
    class Meta:
        model = Image
        
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }
    
    def clean_url(self):
        """
            We'll only allow images end with  "*.jpg" (or .jpeg)
                by simply 'split the str' to get the ext (if not -> error raised)
                
            ( This func is kinda a helper for the following functions :p )
        """
        
        url = self.cleaned_data['url']
        
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        
        if extension not in valid_extensions:
            raise forms.ValidationError('Nope, not a valid file-ext 🤔')
        
        return url
    
    def save(self,
             force_insert=False, force_update=False, commit=True):
        """
            Let's break down the code down below :)
            
            `image`
                An instance with a param (tell Django do NOT commit!)
            
            `image_url`
                simply get the url which was cleaned up (not dup with prev `clean_url`)
            
            `image_name`
                slugify the name & plus the ext (either .jpg or .jpeg, if not -> error)
                
            `response`
                access the image page (ready for being used by `ContentFile`)
                
            `image_inst.image.save`
                image_inst      an instance producted by the 'ImageCreateForm'
                image           the actual HTML widget (in models.py)
                
                ContentFile     file-alike that just take raw content (i.e. .jpg file)
            
        """
        
        image_inst = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        
        image_name = '{}.{}'.format(slugify(image_inst.title),
                                    image_url.rsplit('.', 1)[1].lower())
        
        # download img from the given url
        response = request.urlopen(image_url)
        image_inst.image.save(image_name,
                              ContentFile(response.read()),
                              save=False)
        
        if commit:
            image_inst.save()
        
        return image_inst