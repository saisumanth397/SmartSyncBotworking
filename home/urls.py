from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    
    path('about', views.about,name='about'),
    path('projects', views.projects,name='LogOut'),
    path('login',include('django.contrib.auth.urls')),
    path('contacts', views.contacts,name='contacts'),
    path('',views.home,name='home'),
    path('workbench' ,views.workbench,name='workbench' ),
    path('login', views.projects ,name='login'),
    path('Faq', views.Faq , name='Faq'),
    path('help', views.Help , name='Help'),
]
