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