from django.contrib import admin
from django.urls import path,include
from . import views

# app_name="UserLogin"
urlpatterns=[

    path('',views.login,name='login'),
    path('login',views.login,name='login'),
    path('UserRegistration',views.register,name='register'),
    path('CreateAccount',views.createAccount,name='Account'),

]