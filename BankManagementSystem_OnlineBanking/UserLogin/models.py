from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    mobileNo = models.BigIntegerField()
    # emailAddress = models.EmailField()
    homeAddress = models.TextField()
    accountNo = models.BigIntegerField( unique=True )
    AadharNo = models.BigIntegerField( unique=True )
    IFSC_code = models.CharField(max_length=7, default='ABC1234')
    accBalance = models.BigIntegerField( default=0 )


class Transaction(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    accountNo = models.BigIntegerField()
    TransactionID = models.CharField(max_length=12)
    Amount = models.IntegerField()
