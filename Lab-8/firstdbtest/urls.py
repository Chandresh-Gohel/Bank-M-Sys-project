from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
urlpatterns = [
        path('', views.index, name='index'),
		path('new', views.index, name='index'),
        path('add', views.addstudentinfo, name='add'),
        path('view', views.getstudentinfo, name='add'),
        url('students', views.StudentListView, name ='students'),

        
]