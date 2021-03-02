from django.urls import path
from loginmodule.views import login, auth_view, logout, loggedin, invalidlogin
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
	url(r'^login/$', login),
	url(r'^auth/$', auth_view),
	url(r'^logout/$', logout),
	url(r'^loggedin/$', loggedin),
	url(r'^invalidlogin/$', invalidlogin),
]