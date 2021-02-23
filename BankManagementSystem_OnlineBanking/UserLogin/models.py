from django.db import models

# Create your models here.

class details(models.Model):

    name = models.CharField(max_length=30)
    mobileNo = models.BigIntegerField()
    emailAddress = models.EmailField()
    homeAddress = models.TextField()
    accountNo = models.BigIntegerField( unique=True )
    AadharNo = models.BigIntegerField( unique=True )
    IFSC_code = models.CharField(max_length=7, default='ABC1234')
    accBalance = models.BigIntegerField( default=0 )
    username = models.CharField(max_length=14, blank=True , null=True)
    password = models.CharField(max_length=8,blank=True , null=True)

