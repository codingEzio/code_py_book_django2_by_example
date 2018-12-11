from django.contrib.sitemaps import Sitemap

from .models import Post


class PostSiteMap(Sitemap):
    """
        Just a reminder:
            We're (simply) override
            the (static) attrs of the class 'Sitemap' :P
            
        Some attrs & methods:
        
            changefreq  possible vals: 'always', 'daily', 'yearly' etc.
            
            priority    quotes from 'sitemaps.org'
            
                        Search engines may use this information
                        when selecting between URLs on the same site,
                            so you can use this to increase the likelihood
                            that your most important pages are present in searching.
        
            items       what to include (in the sitemap)
            
            lastmod     the last-mod-time of the post (get from 'items()')
                        the 'updated' is the field from our model 'Posts' :P
    """
    
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.published.all()
    
    def lastmod(self, obj):
        return obj.updated