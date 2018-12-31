import csv
import datetime

from django.contrib import admin
from django.http import HttpResponse

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def export_to_csv(modeladmin, request, queryset):
    """
        The three params are REQUIRED :D
    """
    
    opts = modeladmin.model._meta
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        'attachment;'
        'filename={}.csv'.format(opts.verbose_name)
    )
    
    # Init a CSV file
    #   of course it got a name (ie `opts.verbose_name`)
    writer = csv.writer(response)
    
    # The M-to-M & N-to-M relationship will be excluded :D
    fields = [
        field for field in opts.get_fields()
        if not field.many_to_many and
           not field.one_to_many
    ]
    
    # The header for the CSV file
    writer.writerow(
        [field.verbose_name for field in fields]
    )
    
    for obj in queryset:
        data_row = []
        
        for field in fields:
            value = getattr(obj, field.name)
            
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            
            data_row.append(value)
        writer.writerow(data_row)
    
    return response


export_to_csv.short_description = 'Export to CSV'


def order_detail(obj):
    """

    """
    
    return mark_safe(
        '<a href="{}">View</a>'.format(
            reverse(
                'orders:admin_order_detail', args=[obj.id]
            )
        )
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city',
                    'paid',
                    'created', 'updated',
                    order_detail]
    
    list_filter = ['paid', 'created', 'updated']
    
    inlines = [OrderItemInline]
    
    # csv related
    actions = [export_to_csv]