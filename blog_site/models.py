from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def post_comment(self):
        return Comments.posts.filter(approved_commets=True)

    def get_absolute_url(self):
        return reverse('blog:post_list',kwargs={'pk':self.pk})

    def __str__(self):
        return self.title

class Comments(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True,related_name='posts')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comments = models.BooleanField(default=False)

    def approve_comments(self):
        self.approved_comments = True
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_list',kwargs={'pk':self.pk})
