from django.urls import path
from blog import views

urlpatterns=[
    # path("",views.index, name='index'),
    path("",views.about, name='about'),
    path("seocho",views.seocho, name='seocho'),
    path("duckyang",views.duckyang, name='duckyang'),
    path("post/maps", views.maps, name="maps"),
    path('detectme/',views.detectme,name="detectme"),
    path('info/',views.info,name="info"),
    path('search/',views.search,name="search"),
    path('searchwhole/',views.searchwhole,name="searchwhole"),
    path('sendsns/<int:phonenumber>/',views.sendsns,name="sendsns"),
    path('sns',views.sns,name='sns'),
    path('about/',views.about,name='about'),

]
