from django.shortcuts import render, redirect
from blog.models import *
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django import forms
from django.utils import timezone
from django.core.paginator import Paginator

#웹캠 library
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
#twilio sms
from twilio.rest import Client

#SMS key(이건 절대노출되면 안됨)
account_sid = 'ACc9d44e3405a3b0e7588a8bb3ccad2456'
auth_token = '05eead392a54f50611b7580c0e48bab8' 
client = Client(account_sid, auth_token)

# Create your views here.
def index(req):
    return render(req, "index.html")

class PostDetailView(generic.DetailView):
    model = Post

def maps(req):
    return render(req, 'blog/maps.html')

def info(req):
    driver = Driver.objects.all()
    
    context={
        "driver": driver,
    }

    return render(req, "blog/info.html",context=context)

# 필드명__icontains = 조건값 을 통해 조건값이 포함되는 데이터를 대소문자 구분없이 모두 가져옵니다.

def search(req):
    driver = Driver.objects.all()
    q = req.POST.get('q',"")
    if q:
        driver = driver.filter(carnumber__icontains=q)
        return render(req,'blog/info.html',{'driver':driver,'q':q})
    else:
        return render(req, 'blog/info.html')
    
    
def searchwhole(req):
    driver = Driver.objects.all()
    return render(req,'blog/info.html',{'driver':driver})

def sendsns(req, phonenumber):
    message = client.messages.create( 
    to = "+82"+f"{phonenumber}",
    from_="+13194088767", 
    body="check this out 나는 정상수")

    return redirect("searchwhole")








# 웹캠 비디오스트리밍 코드
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def detectme(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        print("에러입니다...")
        pass
# 여기까지 웹캠 코드

