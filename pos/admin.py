from django.contrib import admin
from pos.models import ProductOrder,SellOrder,Sell,SalesReturn
# Register your models here.

admin.site.register(ProductOrder)
admin.site.register(SellOrder)
admin.site.register(Sell)
admin.site.register(SalesReturn)


