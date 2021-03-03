# Create your models here.
from django.db import models

class book_master(models.Model):
	book_id = models.IntegerField(primary_key=True)
	book_name = models.CharField(max_length = 20)
	book_price = models.IntegerField()