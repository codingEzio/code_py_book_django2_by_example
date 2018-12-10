from django import template
from ..models import Post

register = template.Library()


@register.simple_tag(name='my_post_count')
def total_posts():
    """
        Simply two parts (at least for now :P)
        
        The decorator determines
            what types of content this tag func is
            either simply a string or being used for rendering :P
            
        The return
            the content you wanna return (-> templates)
        
        Oh! Also about the tag name
            
            @register.simple_tag()              =>  name of the func being decoed
            @register.simple_tag(name='my_tag') =>  simply 'my_tag' (better, huh?)
    """
    
    return Post.published.count()