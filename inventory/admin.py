from django.contrib import admin
from inventory.models import Product,Category,ProductReturn
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductReturn)