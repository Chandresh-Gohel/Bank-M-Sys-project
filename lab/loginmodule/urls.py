from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from loginmodule.views import login, auth_view, logout,loggedin, invalidlogin
from django.contrib.auth import views as auth_views

urlpatterns = [
	url('login/', login),
	url('auth/', auth_view),
	url('logout/', logout),
	url('loggedin/', loggedin),
	url('invalidlogin/', invalidlogin),
]