from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from UserLogin.models import details
from Accounts.models import transaction,Contactus
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from decouple import config
import smtplib
import random
import string


def home(request):
    return render(request,'home.html')


def viewBalance(request):
    user = details.objects.get(user_id=request.user.id)
    accBalance = user.accBalance
    accNumber = user.accountNo
    accountNo = "XXX"+str(accNumber)[3:]
    Name = user.name
    userdata = {'accBalance':accBalance,'accountNo':accountNo,'Name':Name}
    return render(request,'viewBalance.html',userdata)

def viewProfile(request):
    user=details.objects.get(user_id=request.user.id)
    obj=User.objects.get(id=user.user_id)
    Email = obj.email
    if request.method=='POST':
        email= request.POST['inputEmail']
        MobileNo= request.POST['inputmobile']
        Address= request.POST['inputAddress']
        user.mobileNo=MobileNo
        user.homeAddress=Address
        user.save()
        obj.email=email
        obj.save()
        messages.success(request,"Your Details Updated Successfully ..")
        return render(request,'viewProfile.html',{'user':user,'Email':Email})
    else:
        return render(request,'viewProfile.html',{'user':user,'Email':Email})

def create_TransactionID():
    return ''.join(random.choices(string.digits,k=9))



def makeTransaction(request):
    if request.method=='POST':
        beneficiaryName = request.POST['BeneficiaryName']
        BeneficiaryAccountNumber = request.POST['AccountNumber']
        ReAccountNumber = request.POST['ReAccountNumber']
        TransactionAmount = int(request.POST['TransactionAmount'])

        password = request.POST['password']
        user = User.objects.get(id=request.user.id)
        username = user.username
        user = auth.authenticate(username=username,password=password)

        if (BeneficiaryAccountNumber==ReAccountNumber):
            AccountHolder = details.objects.get(user_id=request.user.id)
            beneficiary = details.objects.filter(accountNo=BeneficiaryAccountNumber).exists()
            print("+*+",beneficiary)
            if beneficiary is not False:
                beneficiary = details.objects.get(accountNo=BeneficiaryAccountNumber)
                if user is not None:
                    if(int(AccountHolder.accBalance) > 0 and int(TransactionAmount<=AccountHolder.accBalance)):    
                        AccountHolder.accBalance = int(AccountHolder.accBalance - TransactionAmount)
                        AccountHolder.save()
                        beneficiary.accBalance = int(beneficiary.accBalance + TransactionAmount)
                        beneficiary.save()
                        print(AccountHolder.accBalance)
                        print(beneficiary.accBalance)

                        TransactionID = "YoB"+str(create_TransactionID())

                        Transaction1 = transaction.objects.create(accountNumber=AccountHolder.accountNo,Name=AccountHolder.name,TransactionID=TransactionID ,TransactionAmount=-TransactionAmount,Balance=beneficiary.accBalance ,user_id=beneficiary.user_id)
                        Transaction1.save()
                        Transaction2 = transaction.objects.create(accountNumber=beneficiary.accountNo,Name=beneficiary.name,TransactionID=TransactionID,TransactionAmount=TransactionAmount,Balance=AccountHolder.accBalance,user_id=request.user.id)
                        Transaction2.save()
                        messages.success(request,'<font style="color: rgb(75, 224, 75);">Your Transaction complete successful</font>', extra_tags='safe')
                        send_debit_mail(request)
                        send_credit_mail(request)
                        return redirect('/Accounts/makeTransaction')
                    else:
                        return redirect('/Accounts/viewBalance')
                else:
                    messages.info(request,"May your login password is wrong.")
                    return redirect('/Accounts/makeTransaction')
            else:
                messages.info(request,"May some details>(i.e beneficiary A/C) is wrong")
                return redirect('/Accounts/makeTransaction')
        else:
            messages.info(request,"Account number doesn't match with eachother")
            return redirect('/Accounts/makeTransaction')
    else:
        return render(request,'makeTransaction.html')


def send_credit_mail(request):
    
    accountNumber= request.POST['AccountNumber']
    AccountHolder =details.objects.get(accountNo=accountNumber)
    AccHolderName = AccountHolder.name
    TransactionAmount = str(request.POST['TransactionAmount'])
    subject =  AccHolderName + ",Your Transactions done successfully. :) "
    user=User.objects.get(id=AccountHolder.user_id)
    mail=user.email
    sender=config('SENDERMAIL')#sender@mail
    password=config('PASSWORD')#sender@mail&password
    messages="\n"+subject+"\nRupees " + TransactionAmount + "/- is Credited to Your account."
    if subject:
        try:
            server = smtplib.SMTP('smtp.mail.yahoo.com',587)
            server.ehlo()
            server.starttls()
            server.login(sender,password)
            server.sendmail(sender,mail,messages)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')


def send_debit_mail(request):
    
    AccountHolder =details.objects.get(user_id=request.user.id)
    AccHolderName = AccountHolder.name
    TransactionAmount = str(request.POST['TransactionAmount'])

    subject =  AccHolderName + ",Your Transactions done successfully. :) "
    user=User.objects.get(id=request.user.id)
    mail=user.email
    sender=config('SENDERMAIL')#sender@mail
    password=config('PASSWORD')#sender@mail&password
    messages="\n"+subject+"\nRupees " + TransactionAmount + "/- is Debited from Your account."
    if subject:
        try:
            server = smtplib.SMTP('smtp.mail.yahoo.com',587)
            server.ehlo()
            server.starttls()
            server.login(sender,password)
            server.sendmail(sender,mail,messages)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
    else:
        return HttpResponse('Make sure all fields are entered and valid.')




def transactionHistory(request):
    user = details.objects.get(user_id=request.user.id)
    histobj=transaction.objects.filter(user_id=request.user.id)
    print(user.name,user.accountNo)
    return render(request,'transactionHistory.html',{'history':histobj,'user':user})

def delsession(request):
    del request.session['name']
    del request.session['accNo']
    return redirect('/UserRegistration')

def giveIssue(request):
    user = details.objects.get(user_id=request.user.id)
    username=user.name
    useraccountnumber=user.accountNo
    usermobile=user.mobileNo
    #useremail=user.email
    useraddress=user.homeAddress
    userdata={'username':username,'useraccountnumber':useraccountnumber,'usermobile':usermobile,'useraddress':useraddress}
    return render(request, 'contactus.html',userdata)

def contactus(request):
    if request.method=='POST':
        username=request.POST.get('inputUserName')
        useraccountNo=request.POST.get('inputaccountnumber')
        mobileNo = request.POST.get('inputmobile')
        #emailAddress = request.POST.get('inputEmail')
        homeAddress = request.POST.get('inputAddress')
        issuewith = request.POST.get('issuewith')
        userIssue= request.POST.get('userIssue')
        inputZip=request.POST.get('inputZip')
        #print(username,useraccountNo,mobileNo,homeAddress,issuewith,userIssue,inputZip)
        prob = Contactus.objects.create(AccountHolder=username,AccountNumber=useraccountNo,MobileNumber=mobileNo,Address=homeAddress,IssueType=issuewith,Issue=userIssue,PostalZip=inputZip)
        prob.save()
        return redirect('/Accounts/home')
    else:
        HttpResponse("Bad Error in contactus")
        return redirect('/Accounts/home')
    
def send_email(request):
    account=request.session['accNo']
    AccHolderName=request.session['name']
    IFSC="ABC1234"
    subject = AccHolderName+" your Account is created. :)"
    obj=details.objects.get(accountNo=account)
    user=User.objects.get(id=obj.user_id)
    mail=user.email
    sender=config('SENDERMAIL')#sender@mail
    password=config('PASSWORD')#sender@mail&password
    messages="\n"+subject+"\nYour Account Number is:- "+str(account)+"\nYour IFSC Code is- "+str(IFSC)+"\nThank You."
    if subject:
        try:
            server = smtplib.SMTP('smtp.mail.yahoo.com',587)
            server.ehlo()
            server.starttls()
            server.login(sender,password)
            server.sendmail(sender,mail,messages)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return redirect('/Accounts/delsession')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')

