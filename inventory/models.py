import os
import uuid
from io import BytesIO
from barcode import ITF,EAN8
from django.db import models
from datetime import datetime
from PIL import Image,ImageOps
from django.urls import reverse
from django.core.files import File
from barcode.writer import ImageWriter
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.shortcuts import HttpResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
    
    CATEGORY_CHOICES = (
        ('shirt', 'Shirt'),
        ('pant', 'Pant'),
        ('tshirt', 'T shirt'),
    )

    name = models.CharField(max_length=200,blank=False)
    # category=models.ForeignKey(Category,on_delete=models.DO_NOTHING,default=1)
    category=models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    color=models.CharField(max_length=50,choices=COLOR_CHOICES)
    size=models.CharField(max_length=50,choices=SIZE_CHOICES)
    quantity=models.IntegerField(default=1,validators=[MinValueValidator(1)])
    image=models.ImageField(upload_to="product_images/",blank=False)
    productioncost=models.FloatField(default=0.0)
    transportcost=models.FloatField(default=0.0)
    additionalcost=models.FloatField(default=0.0)
    totalcost=models.FloatField(default=0.0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    qcode=models.CharField(max_length=20,default="",blank=True)
    barcode=models.ImageField(blank=True,null=True,upload_to='product_barcode/')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def save(self, *args, **kwargs):
        if not self.id:
            super(Product, self).save(*args, **kwargs)

        self.totalcost = self.productioncost + self.transportcost + self.additionalcost
        super(Product, self).save(*args, **kwargs)


        
     
    def delete(self, *args, **kwargs):
        # Delete the barcode image before deleting the product
        self.delete_barcode_image()
        super(Product, self).delete(*args, **kwargs)
    
    def delete_barcode_image(self):
        if self.barcode:
            image_path = os.path.join('media', self.barcode.name)
            if os.path.exists(image_path):
                os.remove(image_path)
                    
    def __str__(self):
        return f"{self.name}"
    
    def get_absolute_url(self):
        return reverse("App_inventory:editproduct", kwargs={"id": self.id})

@receiver(pre_save, sender=Product)
def generate_product_barcode(sender, instance, **kwargs):
    if not instance.barcode:
        code = EAN8(str(instance.uuid.int), writer=ImageWriter())
        image_width = 288
        image_height = 140
        buffer = BytesIO()
        code.write(buffer)
        buffer.seek(0)
        barcode_image = Image.open(buffer)

        # Calculate the space height and create a new blank image with the desired dimensions
        space_height = 20  # Adjust this value to set the desired space height
        new_image_height = barcode_image.height + space_height
        new_image = Image.new('RGB', (barcode_image.width, new_image_height), color='white')

        # Paste the barcode image onto the new image with space at the top
        new_image.paste(barcode_image, (0, space_height))

        # Save the modified barcode image
        directory = 'media/product_barcode'
        if not os.path.exists(directory):
            os.makedirs(directory)
        filename = f"{instance.uuid}_barcode.png"
        barcode_path = os.path.join(directory, filename)
        new_image.save(barcode_path, 'PNG')
        instance.barcode.name = barcode_path
        instance.qcode = code.get_fullcode()
        instance.save()  
class ProductReturn(models.Model):
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING)
    addedby=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField(default=1)
    crested=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product.name} - {self.addedby.username}"
    
    
    def get_absolute_url(self):
        return reverse("App_inventory:editreturnproduct", kwargs={"id": self.id})


class Notifications(models.Model):
    user=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    message=models.CharField(max_length=150)
    created=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.user)    
    
    
    def save(self, *args, **kwargs):
        # Call the original save() method
        super().save(*args, **kwargs)

        subject = 'Product Removed Notification'
        email_message =self.message
        to_email='jstutul33@gmail.com'
        email = EmailMessage(
            subject, email_message, to=[to_email]
        )
        email.send()