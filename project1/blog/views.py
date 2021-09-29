from django.shortcuts import render, redirect
from blog.models import Category, Post
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.
def index(req):
    post_latest = Post.objects.order_by("-createDate")[:6]
    
    context={
        "post_latest": post_latest,
    }

    return render(req, "index.html",context=context)
    

class PostDetailView(generic.DetailView):
    model = Post


def detail(req, post_id):
    post_detail = Post.objects.get(id = post_id)
    return render(req, 'blog/post_detail.html', {'post':post_detail})
    
def create(req):
    return render(req, 'blog/create.html')

def create2(req):
    post = Post()
    post.title = req.GET['title']
    post.title_image = req.GET['image']
    post.content = req.GET['body']
    post.updateDate = timezone.datetime.now()
    
    post.save()
    return redirect('/blog')
    
def register(req):
    return render(req, 'blog/register.html')

def maps(req):
    return render(req, 'blog/maps.html')


