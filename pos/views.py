import math 
from django.core import serializers
from django.shortcuts import render,get_object_or_404
from inventory.models import Product
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='App_Auth:login')
def poshome(request):
    context = {
        'category_choices': Product.CATEGORY_CHOICES,
        'color_choices': Product.COLOR_CHOICES,
        'size_choices': Product.SIZE_CHOICES,
    }
    return render(request,'pos/pos/index.html',context)

@login_required(login_url='App_Auth:login')
def get_product_api(request):
    barcode = request.GET.get('barcode')
    category = request.GET.get('category')
    color = request.GET.get('color')
    size = request.GET.get('size')
    print(category,color,size,barcode)
    products = Product.objects.all()
    if barcode:
        barcode = math.sqrt(int(barcode) - 10000)
        products = products.filter(id=barcode)
    if category:
        products = products.filter(category=category)
    if color:
        products = products.filter(color=color)
    if size:
        products = products.filter(size=size)
    serialized_products = serializers.serialize('json', products)
    data = {
        "products": serialized_products,
    }
    return JsonResponse(data, safe=False)


@login_required(login_url='App_Auth:login')
def get_single_product_api(request):
    pid = request.GET.get('id')
    print(pid)
    try:
        products = get_object_or_404(Product,id=pid)
        product={
            'id':products.id,
            'name':products.name,
            'image':products.image.url,
            'quantity':products.quantity,
            'size':products.size,
            'color':products.color,
        }
    except:
        product=[]  
    data = {
        "products": product,
    }
    return JsonResponse(data, safe=False)

