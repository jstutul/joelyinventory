from django.urls import path
from inventory.views import *
app_name = 'App_inventory'
urlpatterns = [
  path('',dashboard,name="dashboard"),
  path('users',userlist,name="userslist"),
  path('adduser',adduser,name="adduser"),
  path('deleteuser',deleteuserdata,name="deleteuser"),
  path('edituser/<int:id>',edituserdata,name="edituser"),
  
  ##product part start
  path('products',viewproduct,name="products"),
  path('product/add',addproductview,name="addproduct"),
  path('product/edit/<int:id>', editproductview, name='editproduct'),
  path('product/delete', deleteproductview, name='deleteproduct'),
  
  ##end
]