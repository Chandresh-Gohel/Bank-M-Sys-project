from django.contrib import admin
from django.urls import path,include
from . import views

app_name="UserLogin"
urlpatterns=[

    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('UserRegistration',views.register,name='register')
]