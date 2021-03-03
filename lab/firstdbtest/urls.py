from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
urlpatterns = [
	url('addstudentinfo/', views.addstudentinfo),
	url('getstudentinfo/', views.getstudentinfo),
	url('addsuccess/', views.addsuccess),
	url('students/', views.StudentListView, name ='students'),
]