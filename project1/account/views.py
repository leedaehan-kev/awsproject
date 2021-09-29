from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(req):
    if req.method =="POST":     
        username = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(username=username).exists():
            return render(req,'signup.html',{'error':"이미 존재하는 사용자입니다."})
            
        user = User.objects.create_user(username,password=password)
        
        auth.login(req,user)
        return redirect('/')
    else:
        return render(req,'signup.html')

def login(req):
    if req.method=="POST":
        username=req.POST['email']
        password=req.POST['password']
        user=auth.authenticate(req,username=username, password=password)
        if user is not None:
            auth.login(req,user)
            return redirect('/')
        else:
            return render(req,'login.html',{'error':"이메일 혹은 패스워드가 일치하지 않습니다"})
    else:
        return render(req, 'login.html')

def logout(req):
    auth.logout(req)
    return redirect('/')