from django.urls import path
from authuser.views import *
app_name = 'App_Auth'
urlpatterns = [
  path('login',loginview,name="login"),
  path('logout',logoutview,name="logout"),

 
]
