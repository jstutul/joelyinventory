from django.contrib import admin
from inventory.models import Product,Category,ProductReturn,Notifications
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductReturn)
admin.site.register(Notifications)