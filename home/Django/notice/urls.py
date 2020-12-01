from django.urls import path
from . import views

urlpatterns = [
    path('start_notice', views.start_notice, name='start_notice'),
    path('search_notice', views.search_notice, name='search_notice'),
    path('select_notice', views.select_notice, name='select_notice'),
]
