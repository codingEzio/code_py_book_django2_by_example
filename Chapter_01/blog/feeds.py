from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post


class LatestPostsFeed(Feed):
    """
        Similar to 'sitemap',
            what we're doing is also edit the things in RSS
            the only diff is that we're using code (rather than XML)
    """
    
    title = 'My blog'
    link = '/blog/'
    description = 'New posts of my blog :P'
    
    def items(self):
        return Post.published.all()[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body, 30)