from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=50)
    dob=models.DateField()
    class Meta:
        db_table="firstdbtest_student"