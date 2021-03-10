from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class details(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    BirthDate = models.DateField()
    mobileNo = models.BigIntegerField()
    homeAddress = models.TextField()
    accountNo = models.BigIntegerField( unique=True )
    AadharNo = models.BigIntegerField( unique=True )
    IFSC_code = models.CharField(max_length=7, default='ABC1234')
    accBalance = models.BigIntegerField( default=0 )

    def __str__(self):
        return self.name
