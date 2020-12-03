from django.urls import path
from . import views

urlpatterns = [
    path('start_club', views.start_club, name='start_club'),
    path('select_club', views.select_club, name='select_club'),
    path('search_club', views.search_club, name='search_club'),
]
