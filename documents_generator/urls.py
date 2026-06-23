from django.urls import path
from . import views

app_name = 'gai'

urlpatterns = [
    path('', views.index, name='index'),
    path('generate', views.generate_document, name='generate_document'),
]