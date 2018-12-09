from django.contrib import admin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
        By using the decorator,
            we still maintaining the functionality as before.
        
        Other than that,
            we're gonna customize the 'admin' (the spclass being passed in)
    """
    
    # Columns for posts
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    
    # Filtering & searching
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    
    # Prepopulating the 'slug' field
    #   with the input of the 'title' field (auto typing onto it)
    prepopulated_fields = {'slug': ('title',)}
    
    # It'll display a lookup widget ("a select-box interface")
    #   which it's much better than a drop-down one.
    #   Just imagine that you got thousands of users or more!
    raw_id_fields = ('author',)
    
    # All
    # 2018
    # 2018 Dec.
    # 2018 Dec. 6
    date_hierarchy = 'publish'
    
    # Ordering by the 1st one
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')