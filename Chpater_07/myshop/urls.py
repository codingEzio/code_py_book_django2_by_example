from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin

from django.urls import path, include

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    
    # These routes MUST be put before the 'shop.urls'
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('coupons/', include('coupons.urls', namespace='coupons')),
    
    # Third-party translation library
    path('rosetta/', include('rosetta.urls')),
    
    path('', include('shop.urls', namespace='shop')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)