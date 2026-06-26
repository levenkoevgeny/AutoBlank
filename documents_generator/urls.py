from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'gai'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate_document, name='generate_document'),
    path('feedback', views.feedback, name='feedback'),
    path('download-template', views.download_template, name='download_template'),
    path('download', views.download_page, name='download_page'),
    path('sitemap.xml', views.sitemap_xml, name='sitemap_xml'),
    path('yandex_519162dd5d6ded9a.html', views.yandex_servise, name='yandex_servise'),
    path('favicon.ico', views.favicon_view, name='favicon_view'),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt',
        content_type='text/plain'
    ), name='robots_txt'),
]