from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class student_res(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='students')
    std = models.CharField(max_length=300)
    phone = models.CharField(max_length=300)