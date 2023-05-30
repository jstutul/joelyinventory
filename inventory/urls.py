from django.urls import path
from inventory.views import *
app_name = 'App_inventory'
urlpatterns = [
  path('',dashboard,name="dashboard"),
  path('users',userlist,name="userslist"),
  path('adduser',adduser,name="adduser"),
  path('deleteuser',deleteuserdata,name="deleteuser"),
]

