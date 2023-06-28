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
  path('product/remove', deleteproductview, name='removeproduct'),
  ##end
  
  ##removed product part
  path('remove/products',restoreviewproduct,name="restoreproducts"),
  path('product/restore', restoreremovedproductview, name='backrestoreproduct'),
  path('product/delete', deleteremovedproductview, name='deleteproduct'),
  ##end
  
  ##return product part
  path('product/quantity/', getproductquantity, name='pquantity'),
  path('return/products',returnproductview,name="returnproduct"),
  path('return/add', addreturnproduct, name='addreturnproduct'),
  path('return/edit/<int:id>', editreturnproduct, name='editreturnproduct'),
  ##end
  path('product/barcode',barcodeview,name="barcode"),
  path('product/barcode/image',getbarcodeimage,name="getbarcodeimg"),
  
  ## sales
  path('sales',Saleview,name='sale'),
  path('sale-details/<int:id>',SaleDetailsview,name='saledetails'),
  path('sale-update/<int:id>',SalesEditview,name='saleedit'),
  
  ##notification
  path("notifications",NotificationView,name="notifications"),
  path("notifications/delete/<int:id>",NotificationDeleteView,name="notificationsdelete"),
  
  
  
]