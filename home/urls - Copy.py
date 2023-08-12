from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.projects),# 2) the request then comes here and this then directs to project function in views.py file in home folder 
    path('about', views.about,name='about'),
    path('projects', views.projects,name='LogOut'),
    path('',include('django.contrib.auth.urls')),
    path('contacts', views.contacts,name='contacts'),
    path('home',views.home,name='home'),
    path('workbench' ,views.workbench,name='workbench' ),
]
