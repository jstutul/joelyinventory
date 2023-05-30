from django.contrib import admin
from django.urls import path,include
admin.site.site_title = 'N-tech Solution'
admin.site.site_header = 'N-tech Solution'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('inventory.urls')),
    path('',include('pos.urls')),
    path('auth/',include('authuser.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
