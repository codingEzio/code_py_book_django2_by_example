from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSiteMap(Sitemap):
    """
        Just a reminder:
            We're (simply) override
            the (static) attrs of the class 'Sitemap' :P
    """
    
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated