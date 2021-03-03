from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib import messages
from UserLogin.models import details

# Create your views here.

def home(request):
    return render(request,'home.html')


def AccNoDisplay(request):
    AccHolderName = request.session['name']
    AccountNo=request.session['accNo']
    if 'name' in request.session:
        param={'name':AccHolderName,'AccountNo':AccountNo} 
        return render(request,'AccNoDisplay.html',param)
    else:
        return HttpResponse("Error 404")
    return redirect('/CreateAccount')


def viewBalance(request):
    user = details.objects.get(user_id=request.user.id)
    accBalance = user.accBalance
    accNumber = user.accountNo
    accountNo = "XXX"+str(accNumber)[3:]
    Name = user.name
    userdata = {'accBalance':accBalance,'accountNo':accountNo,'Name':Name}
    return render(request,'viewBalance.html',userdata)

def makeTransaction(request):
    return render(request,'makeTransaction.html')


def delsession(request):
    del request.session['name']
    del request.session['accNo']
    return redirect('/UserRegistration')
