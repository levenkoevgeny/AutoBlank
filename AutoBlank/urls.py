from django.contrib import admin
from django.urls import path, include
from django.views.defaults import page_not_found

from django.conf import settings
from django.conf.urls.static import static


def custom_404(request, exception):
    return page_not_found(request, exception, template_name='404.html')


handler404 = custom_404

urlpatterns = [
    path('', include('documents_generator.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)