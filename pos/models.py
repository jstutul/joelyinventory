from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product



class ProductOrder(models.Model):
    PAYMENT_STATUS = (
        ('approve', 'Approve'),
        ('pending', 'Pending'),
        ('cashondelivery', 'Cash On Delivery'),
    )
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True,auto_now=False)

    def __str__(self):
        return f"Product Order - {self.product.name}"
 
    def get_total(self):
        # prd=ProductOrder.objects.get(id=self.id)
        return self.price*self.quantity
    
    def save(self, *args, **kwargs):
        # Check if the product with the same color and size is available in stock
        if self.product.quantity < int(self.quantity) or self.product.color != self.color or self.product.size != self.size:
            raise ValueError(f"{self.product.name} is not available in the desired color and size or insufficient quantity")
        super().save(*args, **kwargs)
        # Update the quantity of the associated product
        self.product.quantity -= int(self.quantity)
        self.product.save()

class SellOrder(models.Model):
    PAYMENT_STATUS = (
        ('approve', 'Approve'),
        ('pending', 'Pending'),
        ('cashondelivery', 'Cash On Delivery'),
    )
    product=models.ManyToManyField(ProductOrder,related_name="productorder")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default='approve')
    is_order = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)


    def __str__(self):
        return f"SellOrder {self.id}"

    def add_product(self, product_order):
        self.product.add(product_order)

    def remove_product(self, product_order):
        self.product.remove(product_order)
        
class Sell(models.Model):
    PAYMENT_STATUS = (
        ('approve', 'Approve'),
        ('pending', 'Pending'),
        ('cashondelivery', 'Cash On Delivery'),
    )
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING,default=1)
    order=models.ForeignKey(SellOrder,on_delete=models.DO_NOTHING)
    customer=models.CharField(max_length=50)
    phone=models.CharField(max_length=20,blank=True)
    paymentstatus=models.CharField(max_length=50,choices=PAYMENT_STATUS, default='approve')
    address=models.TextField(null=True, blank=True)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return self.customer
    
    