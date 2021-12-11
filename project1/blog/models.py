from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.base import ModelState
from django.db.models.deletion import Collector
from django.db.models.fields import DateTimeField


# Create your models here.

#블로그 글(제목, 작성일, 대표이미지, 내용)
class Post(models.Model):
    title = models.CharField(max_length=200)
    title_image = models.ImageField(blank=True)
    content = models.TextField()
    createDate = models.DateTimeField(auto_now_add=True)
    updateDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    #1번 글의 경우 ->post/1
    def get_absolute_url(self):
        return reverse("post", args=[str(self.id)])

    def summary(self):
        return self.title[:20]



class CarNumber(models.Model):
    carnumber = models.CharField(max_length=100,primary_key=True)
    date = models.DateField(auto_now_add=True,null=True)
    location = models.CharField(max_length=30)
    locationnumber = models.CharField(max_length=200)
    
    def __str__(self):
        return self.carnumber


class Driver(models.Model):
    name = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=15)
    carnumbers = models.CharField(max_length=20)
    count = models.IntegerField()

    def __str__(self):
        return self.carnumbers
