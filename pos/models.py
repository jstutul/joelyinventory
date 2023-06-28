from django.db import models
from django.contrib.auth.models import User
from inventory.models import Product



class ProductOrder(models.Model):
    seller = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created=models.DateTimeField(auto_now=True)
    updated=models.DateTimeField(auto_now_add=True,auto_now=False)
    order  = models.BooleanField(default=False)

    def __str__(self):
        return f"Product Order - {self.product.name}"
 
    def get_total(self):
        # prd=ProductOrder.objects.get(id=self.id)
        return self.price*self.quantity
    
    def save(self, *args, **kwargs):
        print(self.quantity,self.product.quantity)
        # if self.product.quantity < int(self.quantity):
        #     raise ValueError(f"{self.product.name} is not available in the desired color and size or insufficient quantity")
        super().save(*args, **kwargs)
        self.product.save()

class SellOrder(models.Model):
    product=models.ManyToManyField(ProductOrder,related_name="productorder")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50)
    is_payment = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True, auto_now=False)


    def __str__(self):
        return f"SellOrder {self.id}"

    def add_product(self, product_order):
        self.product.add(product_order)

    def remove_product(self, product_order):
        self.product.remove(product_order)
        
    # def sales_remove_product(self, product_order):
        # self.product.remove(product_order)
        # product_order.product.quantity -= product_order.quantity
        # product_order.product.save()
        # self.subtotal -= product_order.get_total()
        # self.total -= product_order.get_total()
        # self.save()    
        
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
            
class SalesReturn(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    prodcut=models.ForeignKey(ProductOrder,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(default=1)
    customer=models.CharField(max_length=100)
    mobile  =models.CharField(max_length=20,blank=True)
    created=models.DateTimeField(auto_now=True,auto_now_add=False)
    updated=models.DateTimeField(auto_now=False,auto_now_add=True)  
    
    
    def __str__(self):
        return f"{self.customer}"  