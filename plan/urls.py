from django.urls import path
from . import views

urlpatterns = [
    path('', views.message, name='message'),
    path('change_plan', views.change_plan, name='change_plan'),
    path('test', views.test, name='test'),
    path('start_plan', views.start_plan, name='start_plan'),
    path('delete_plan', views.delete_plan, name='delete_plan'),
    path('check_plan', views.check_plan, name='check_plan'),
    path('check_plan_date', views.check_plan_date, name='check_plan_date'),
]
