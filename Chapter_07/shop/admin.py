from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    """
        For the "translated_fields", you need to
            use `get_prepopulated_fields` instead of `prepopulated_fields`
        
        Since it provides the same functionality,
            there's no difference actually, just a different way to get it :P
    """
    
    list_display = ['name', 'slug']
    
    def get_prepopulated_fields(self, request, obj=None):
        return { 'slug': ('name',) }


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    
    def get_prepopulated_fields(self, request, obj=None):
        return { 'slug': ('name',) }