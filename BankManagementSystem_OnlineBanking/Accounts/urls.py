from django.contrib import admin
from django.urls import path,include
from . import views

# app_name ="Accounts"

urlpatterns=[

    path('home',views.home,name='home'),
    path('AccNoDisplay',views.AccNoDisplay,name='AccNoDisplay'),
    path('delsession',views.delsession,name='delsession'),
    path('viewBalance',views.viewBalance,name='viewBalance'),
    path('makeTransaction',views.makeTransaction,name='makeTransaction'),
]