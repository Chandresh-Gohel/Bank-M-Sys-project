from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf

def login(request):
	c = {}
	c.update(csrf(request))
	return render('login.html', c)

def auth_view(request):
	username = request.POST.get('username','')
	password = request.POST.get('password','')
	user = auth.authenticate(username = username, password = password)

	if user is not None:
		auth.login(request, user)
		return HttpResponseRedirect('/loginmodule/loggedin/')
	else:
		 return HttpResponseRedirect('/loginmodule/invalidlogin/')
def loggedin(request):
	return render('loggedin.html', {"full_name":request.user.username})

def invalidlogin(request):
	return render('invalidlogin.html')

def logout(request):
	auth.logout(request)
	return render('logout.html')



# Create your views here.

