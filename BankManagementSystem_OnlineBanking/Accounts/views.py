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
    if request.method=='POST':
        beneficiaryName = request.POST['BeneficiaryName']
        BeneficiaryAccountNumber = request.POST['AccountNumber']
        ReAccountNumber = request.POST['ReAccountNumber']
        TransactionAmount = int(request.POST['TransactionAmount'])
        if (BeneficiaryAccountNumber==ReAccountNumber):
            AccountHolder = details.objects.get(user_id=request.user.id)
            beneficiary = details.objects.filter(accountNo=BeneficiaryAccountNumber).exists()
            print("+*+",beneficiary)
            if beneficiary is not False:
                beneficiary = details.objects.get(accountNo=BeneficiaryAccountNumber)
                if(int(AccountHolder.accBalance) > 0 ):    
                    AccountHolder.accBalance = int(AccountHolder.accBalance - TransactionAmount)
                    AccountHolder.save()
                    beneficiary.accBalance = int(beneficiary.accBalance + TransactionAmount)
                    beneficiary.save()
                    print(AccountHolder.accBalance)
                    print(beneficiary.accBalance)

                    Transaction1 = transaction.objects.create(accountNumber=AccountHolder.accountNo,Name=AccountHolder.name,TransactionID="xyx",TransactionAmount=TransactionAmount,Balance=AccountHolder.accBalance ,user_id=beneficiary.user_id)
                    Transaction1.save()
                    Transaction2 = transaction.objects.create(accountNumber=beneficiary.accountNo,Name=beneficiary.name,TransactionID="xyx",TransactionAmount=-TransactionAmount,Balance=beneficiary.accBalance,user_id=request.user.id)
                    Transaction2.save()
                    messages.success(request,'<font style="color: rgb(75, 224, 75);">Your Transaction complete successful</font>', extra_tags='safe')
                    return redirect('/Accounts/makeTransaction')
                else:
                    return redirect('/Accounts/viewBalance')
            else:
                messages.info(request,"May some details>(i.e beneficiary A/C) is wrong")
                return redirect('/Accounts/makeTransaction')
        else:
            messages.info(request,"Account number doesn't match with eachother")
            return redirect('/Accounts/makeTransaction')
    else:
        return render(request,'makeTransaction.html')


def transactionHistory(request):
	user = details.objects.get(user_id=request.user.id)
	histobj=transaction.objects.filter(user_id=request.user.id)
	Username=user.name
	useraccountnumber=user.accountNo
	#print(user_id)
	return render(request,'transactionHistory.html',{'history':histobj,'Username':Username,'YourAccountNumber':useraccountnumber})

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
    messages="\n"+subject+"\nYour Account Number is:- "+str(account)+"\nYour IFSC Code is- "+str(IFSC)
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

