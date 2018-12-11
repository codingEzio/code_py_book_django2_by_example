from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

import markdown

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


@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """
        As its name suggests,
            it was used to "display some content by rendering another template".
            
        A simple comparison,
            complete    <html> ... h p div ... </html>
            partial     e.g. <li> ... </li> (without the whole DOM)
            
        About the code
            the param `count` simply allow you to name 'how many posts were shown'.
    """
    
    latest_posts = Post.published.order_by('-publish')[:count]
    return { 'latest_posts': latest_posts }


@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
            total_comments=Count('comments')
    ).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    """
        The outside param 'name' is similar to "tag" (in 'usage')
            which it'll determines how you use it, e.g. {{ THING | FILTER }}.
        
        Just a reminder
            for tag,    {% my_post_count %}
            for filter, {{ post.body | truncatewords:30 }}
        
        Why using `mark_safe`?
            It simply marks the string as 'safe' for HTML output.
            It was used pretty ?everywhere (in short: ready-for-rendering).
            
        Also, about the 'markdown',
            I simply typed these (& not digging more ...), =_=!
    """
    
    return mark_safe(markdown.markdown(text))

