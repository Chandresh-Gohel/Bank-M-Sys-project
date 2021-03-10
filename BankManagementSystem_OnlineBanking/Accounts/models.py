from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    accountNumber = models.BigIntegerField()
    Name = models.CharField(max_length=25)
    TransactionID = models.CharField(max_length=12)
    TransactionAmount = models.IntegerField()
    Balance = models.IntegerField()
    date = models.DateField(auto_now_add=True)

class Contactus(models.Model):
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    AccountHolder = models.CharField(max_length=25)
    AccountNumber = models.BigIntegerField()
    #email = models.EmailField(max_length=200)
    MobileNumber = models.BigIntegerField()
    Address = models.TextField()
    IssueType = models.CharField(max_length=8)
    Issue = models.TextField()
    PostalZip = models.CharField(max_length=6)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ContactUs"