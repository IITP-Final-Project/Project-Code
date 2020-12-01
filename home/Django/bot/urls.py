"""bot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from helper import views
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^keyboard/?$', views.keyboard),
    url(r'^message/', views.message),
    path('plan/', include('plan.urls')),
    path('timetable/', include('timetable.urls')),
    path('bus_bab/', include('bus_bab.urls')),
    path('notice/', include('notice.urls')),
    path('lecture_rate/', include('lecture_rate.urls')),
    path('club/', include('club.urls')),
]
