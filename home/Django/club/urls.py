from django.urls import path
from . import views

urlpatterns = [
    path('start_club', views.start_club, name='start_club'),
]
