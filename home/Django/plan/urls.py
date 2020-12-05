from django.urls import path
from . import views
from . import hy_views




urlpatterns = [
    path('', views.message, name='message'),
    path('test', views.test, name='test'),
    path('start_plan', views.start_plan, name='start_plan'),
    path('check_plan', views.check_plan, name='check_plan'),
    path('check_plan_date', views.check_plan_date, name='check_plan_date'),
    path('select_change_plan', views.select_change_plan, name='select_change_plan'),
    path('choose_change_plan', views.choose_change_plan, name='choose_change_plan'),
    path('select_delete_plan', views.select_delete_plan, name='select_delete_plan'),

    path('plan_elastic/', hy_views.Schedule, name='hy_Schedule'),
	path('plan_elastic/entire/', hy_views.EntireSchedule, name='hy_EntireSchedule'),
	path('plan_elastic/dailyschedule/', hy_views.DailySchedule, name='hy_DailySchedule'),
	path('plan_elastic/modifyschedule/', hy_views.ModifySchedule, name='hy_ModifySchedule'),
]
