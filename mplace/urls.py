
from django.contrib import admin
from django.urls import path,include
from ajax_select import urls as ajax_select_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ajax_select/', include(ajax_select_urls)),
    path('', include('portal.urls')), 
    path('', include('login.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)