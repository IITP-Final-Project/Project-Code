from django.urls import path
from . import views

urlpatterns = [
    path('test', views.test, name='test'),
    path('start_lecture', views.start_lecture, name='start_lecture'),
    ]
