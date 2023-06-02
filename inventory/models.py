from django.db import models
import os
from datetime import datetime
from django.urls import reverse
# Create your models here.

def product_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.name}.{ext}"
    return os.path.join('product_images', filename)

class Category(models.Model):
    name=models.CharField(max_length=50,blank=False)
    created=models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name

class Product(models.Model):
    SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    )
    COLOR_CHOICES = (
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
    )

    name = models.CharField(max_length=200,blank=False)
    category=models.ForeignKey(Category,on_delete=models.DO_NOTHING,default=1)
    color=models.CharField(max_length=50,choices=COLOR_CHOICES)
    size=models.CharField(max_length=50,choices=SIZE_CHOICES)
    quantity=models.IntegerField(default=1)
    image=models.ImageField(upload_to="product_images/",blank=False)
    productioncost=models.FloatField(default=0.0)
    transportcost=models.FloatField(default=0.0)
    additionalcost=models.FloatField(default=0.0)
    totalcost=models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    qcode=models.CharField(max_length=20,default="",blank=True)
    
    def save(self, *args, **kwargs):
        self.totalcost = self.productioncost + self.transportcost + self.additionalcost
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        formatted_date = self.updated.strftime("%Y-%m-%d %I:%M %p")
        return f"{self.name} - {formatted_date}"
    
    def get_absolute_url(self):
        return reverse("App_inventory:editproduct", kwargs={"id": self.id})
    