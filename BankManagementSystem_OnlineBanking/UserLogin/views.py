from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import details
import random
import string

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/Accounts/home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'login.html')
 
 
def register(request):
    if request.method=='POST':
        userAccNumber=request.POST['userAccNumber']
        userIFSC=request.POST['userIFSC']
        username=request.POST['username']
        password=request.POST['password']
        ConfiPassword=request.POST['ConfiPassword']

        if(password==ConfiPassword):
            if details.objects.filter(accountNo=userAccNumber,IFSC_code=userIFSC).exists():
                u = details.objects.get(accountNo=userAccNumber,IFSC_code=userIFSC)
                user = User.objects.get(id=u.user_id)
                key = request.session['key']
                if user.username==key:
                    user.username=username
                    user.set_password(password)
                    user.save()
            else:
                print("There is no Account with this Account Number")
        else:
            print("Password doesn't matched")
    return render(request,'UserRegistration.html')

def create_AccountNo():
    return ''.join(random.choices(string.digits,k=8))

def createAccount(request):

    if request.method=='POST':
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        fullname=first_name+' '+last_name
        mobileNo = request.POST['mobileNo']
        emailAddress = request.POST['UserEmail']
        AadharCardNo = request.POST['AadharCardNo']
        homeAddress = request.POST['HomeAddress']
        key=first_name+AadharCardNo+last_name

        AccountNo = create_AccountNo()
        unique=False
        while not unique:
            if not details.objects.filter(accountNo=AccountNo).exists():
                unique=True
            else:
                AccountNo= create_AccountNo()


        user = User.objects.create_user(username=key,password=key,email=emailAddress,first_name=first_name,last_name=last_name)
        user.save()
        OtherDetails = details(user=user,accountNo=AccountNo,name=fullname,mobileNo=mobileNo,AadharNo=AadharCardNo,homeAddress=homeAddress)
        OtherDetails.save()
        request.session['name']=fullname
        request.session['accNo']=AccountNo
        request.session['key']=key
        
        return redirect('/Accounts/AccNoDisplay')
    return render(request,'CreateAccount.html')
    
