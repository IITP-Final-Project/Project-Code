from django.urls import path
from . import views

urlpatterns = [
    path('', views.message, name='message'),
    path('change_timetable', views.change_timetable, name='change_timetable'),
]
