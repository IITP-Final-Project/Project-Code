from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('start_bus', views.start_bus, name='start_bus'),
    path('bab', views.bab, name='bab'),
    ]
