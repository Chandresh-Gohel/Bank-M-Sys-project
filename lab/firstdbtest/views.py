from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.template.context_processors import csrf
from firstdbtest.models import Student
from django.contrib.auth.forms import UserCreationForm
from django.db import connection
from django.http import HttpResponseRedirect
from . import views

def getstudentinfo(request):
	c = {}
	c.update(csrf(request))
	return render(request,'addstudentinfo.html', c)

def addstudentinfo(request):
	sname = request.POST.get('studentname','')
	sdate = request.POST.get('birthdate','')
	s = Student(student_name = sname, student_dob=sdate)
	s.save()
	return HttpResponseRedirect('/firstdbtest/addsuccess/')
	
def addsuccess(request):
	return render(request,'addrecord.html')

def StudentListView(request):
	model=Student.objects.all()
	return render(request,'student_list.html',{'student_list':model})
