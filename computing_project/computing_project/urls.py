"""computing_project URL Configuration


"""
from django.contrib import admin
from django.urls import path
from  .views1 import * 
from .views1 import AlertView

urlpatterns = [
    path('admin/',admin.site.urls),
    path('',my_view),
    path('index',my_view),
    path('home',homepage_render),
    path('dashboard',dashboard_render),
    path('logout',logout_view),
    path('test', test_view, name='test'),
    path('graph',graph_view),
    path('get_login', AlertView.as_view(), name='get_login'),
    
]
    


