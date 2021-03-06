from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class transaction(models.Model):
    # user = models.OneToOneField(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    accountNumber = models.BigIntegerField()
    Name = models.CharField(max_length=25)
    # BeneficiaryAccountNumber= models.BigIntegerField()
    TransactionID = models.CharField(max_length=12)
    # beneficiaryName=models.CharField(max_length=25)
    Amount = models.IntegerField()
    # time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)