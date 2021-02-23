from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import details

def index(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        if details.objects.filter(username=username,password=password).exists():
            return redirect('Accounts:home')
        else:
            return redirect('/UserRegistration')
    else:
        return render(request,'index.html')
    
def register(request):
    if request.method=='POST':
        userAccNumber=request.POST['userAccNumber']
        userIFSC=request.POST['userIFSC']
        username=request.POST['username']
        password=request.POST['password']
        ConfiPassword=request.POST['ConfiPassword']

        if(password==ConfiPassword):
            if details.objects.filter(accountNo=userAccNumber,IFSC_code=userIFSC).exists():
                # print(username)
                user = details.objects.get(accountNo=userAccNumber,IFSC_code=userIFSC)
                user.username=username
                user.password=password
                user.save()
            else:
                print("There is no Account with this Account Number")
        else:
            print("Password doesn't matched")
    return render(request,'UserRegistration.html')

