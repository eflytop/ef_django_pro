"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib import admin
# FBV
from . import views
#from .views import home
# CBV
#from .views import DeviceUpdateView, DeviceDetailView

urlpatterns = [
    path('', views.index, name='index'),
    path('device_list/', views.device_list, name='device_list'),
    path('cfg_host/', views.cfg_host, name='cfg_host'),
    path('cfg_verify/', views.cfg_verify, name='cfg_verify'),
    path('cfg_log/', views.cfg_log, name='cfg_log'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('host_add/', views.host_add, name='host_add'),
    path('host_edit/', views.host_edit, name='host_edit'),
    path('host_update/', views.host_update, name='host_update'),
]
