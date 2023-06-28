from django.urls import path
from pos.views import *
app_name = 'App_pos'

urlpatterns = [
    path('',poshome,name="poshome"),
    path('sales-return',salesreturnview,name="salesreturn"),
    #api part
    path('getproduct',get_product_api,name='getproductapi'),
    path('getsingleproduct',get_single_product_api,name='getsingleproduct'),
    path('order',orderview,name='order'),
    path('bill/<int:id>',billview,name='billpage'),
    #new path
    path('additem', save_sales_return, name="add_sales_return"),
]
