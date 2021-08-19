from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from authorization.models import student_res
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Exam(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    subject = models.CharField(max_length=400,blank=True)
    question = models.CharField(max_length=3000)
    option1 = models.CharField(max_length=3000,blank=True)
    optionimg1 = models.ImageField(upload_to='photo/',blank=True,null=True)
    option2 = models.CharField(max_length=3000,blank=True)
    optionimg2 = models.ImageField(upload_to='photo/',blank=True,null=True)
    option3 = models.CharField(max_length=3000,blank=True)
    optionimg3 = models.ImageField(upload_to='photo/',blank=True,null=True)
    option4 = models.CharField(max_length=3000,blank=True)
    optionimg4 = models.ImageField(upload_to='photo/',blank=True,null=True)
    correct = models.CharField(max_length=3000,blank=True)
    correctimg = models.ImageField(upload_to='photo/',blank=True,null=True)



    def __str__(self):
        return self.question

    def get_absolute_url(self):
        return reverse('exam:exam_list')

cho = (('11th','11th'),('12th','12th'),('other','other'))

class Tests(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    std = models.CharField(max_length=30,choices=cho,blank=True,null=True)
    test_name = models.CharField(max_length=1000)
    test_approve = models.BooleanField(default=False)
    test_question = models.ForeignKey(Exam, on_delete=models.CASCADE,null=True)
    test_date = models.DateField(blank=True,null=True,max_length=500)
    test_subject = models.CharField(blank=True,null=True,max_length=300)
    test_time = models.CharField(blank=True,null=True,max_length=300)
    test_end_time = models.CharField(blank=True,null=True,max_length=20)
    slug = models.SlugField(unique=True,blank=True,null=True)

    def slugi(self):
        self.slug = slugify(self.test_name)
        return self.slug

    def get_absolute_url(self):
        return reverse('exam:test_detail',kwargs={'pk':self.pk,'slug':'slug'})

    def __str__(self):
        return self.test_name

class registers(models.Model):
    test = models.ForeignKey(Tests,on_delete=models.CASCADE,related_name='student_registers')
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.CharField(default='59:00',max_length=200,null=True,blank=True)
    end_test = models.BooleanField(default=False)

class ExamAns(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    question = models.ForeignKey(Exam,on_delete=models.CASCADE,null=True,blank=True)
    store = models.CharField(max_length=3000, blank=True, null=True)
    test = models.ForeignKey(Tests,on_delete=models.CASCADE,null=True,blank=True)
