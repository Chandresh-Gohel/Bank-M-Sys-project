from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import generic
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.template.context_processors import csrf
from firstdbtest.models import Student
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.db import connection
from django.http import HttpResponseRedirect
from . import views

# Create your views here.


def index(request):
    return render(request,'firstdbtest/addstudentinfo.html')
def getstudentinfo(request):
    c = {}
    c.update(csrf(request))
    return render(request,'firstdbtest/addstudentinfo.html', c)
def addstudentinfo(request):
    sname = request.POST.get('studentname')
    sdate = request.POST.get('birthdate')
    s = Student(name = sname, dob=sdate)
    s.save()
    return render(request,'firstdbtest/addrecord.html')
def addsuccess(request):
    return render(request,'firstdbtest/addsrecord.html')
	
def StudentListView(request):
	stu=Student.objects.all()
	return render(request,'firstdbtest/student_list.html',{'student_list':stu})
	