from django.db import models

# Create your models here.
class book(models.Model):
    book_id = models.CharField(primary_key=True,max_length=5)
    book_name = models.CharField(max_length=15)
    book_price=models.IntegerField()