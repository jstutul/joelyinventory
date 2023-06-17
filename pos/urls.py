from django.urls import path
from pos.views import *
app_name = 'App_pos'

urlpatterns = [
    path('',poshome,name="poshome"),
    #api part
    path('getproduct',get_product_api,name='getproductapi'),
    path('getsingleproduct',get_single_product_api,name='getsingleproduct'),
    path('order',orderview,name='order'),
    path('bill/<int:id>',billview,name='billpage'),
]
