from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.http import HttpResponse
from django.contrib import messages
from UserLogin.models import details
from Accounts.models import transaction

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

                    Transaction1 = transaction.objects.create(accountNumber=AccountHolder.accountNo,Name=AccountHolder.name,TransactionID="xyx",TransactionAmount=-TransactionAmount,Balance=AccountHolder.accBalance ,user_id=beneficiary.user_id)
                    Transaction1.save()
                    Transaction2 = transaction.objects.create(accountNumber=beneficiary.accountNo,Name=beneficiary.name,TransactionID="xyx",TransactionAmount=TransactionAmount,Balance=beneficiary.accBalance,user_id=request.user.id)
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


def delsession(request):
    del request.session['name']
    del request.session['accNo']
    return redirect('/UserRegistration')
