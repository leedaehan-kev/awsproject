from django.urls import path
from blog import views

urlpatterns=[
    path("",views.index, name='index'),
    path("post/<int:post_id>",views.detail, name="post"),
    path("post/create", views.create, name="create"),
    path("post/create2", views.create2, name="create2"),  
    path("post/maps", views.maps, name="maps"),
    path('detectme/',views.detectme,name="detectme"),
    path('info/',views.info,name="info"),

]
