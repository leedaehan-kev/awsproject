from django.db import models
from django.db.models.deletion import CASCADE
from django.urls import reverse

# Create your models here.
#글의 분류(일상, 유머, 정보)

#블로그 글(제목, 작성일, 대표이미지, 내용, 분류)
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
    carnumber = models.TextField()

class Driver(models.Model):
    name = models.CharField(max_length=10)
    phonenumber = models.CharField(max_length=15)
    carnumber = models.CharField(max_length=20)
    count = models.IntegerField()
    








