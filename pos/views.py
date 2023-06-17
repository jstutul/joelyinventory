import math 
import json
from django.contrib import messages
from pos.models import ProductOrder
from django.core import serializers
from django.http import JsonResponse
from inventory.models import Product
from pos.models import SellOrder,Sell
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect

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

def billview(request,id):
    try:
        order=SellOrder.objects.get(id=id)
        if request.method=="POST":
            customerName=request.POST.get('cname')
            customerPhone=request.POST.get('cphone')
            paymentStatus=request.POST.get('pstatus')
            customerAddress=request.POST.get('caddress')
            
            selldata=Sell(
                user=request.user,
                order=order,
                customer=customerName,
                phone=customerPhone,
                address=customerAddress,
                paymentstatus=paymentStatus
            )
            selldata.save()
            messages.success(request,"Order Completed")
            return redirect('App_pos:poshome')
            
        context={
            'order':order,
            'status': Sell.PAYMENT_STATUS,
        }
    except:
        pass
    return render(request,'pos/pos/bill.html',context)



@csrf_exempt
def orderview(request):
    if request.method == "POST":
        json_data = json.loads(request.body)
        products = json_data["products"]
        subtotal = json_data["subtotal"]
        discount = json_data["discount"]
        total = json_data["total"]
        paymentType = json_data["paymentType"]

        sell_order = SellOrder.objects.create(subtotal=subtotal, discount=discount, total=total, payment_type=paymentType)
        # Create a ProductOrder for each product in the request
        for product_data in products:
            product_order = ProductOrder(
                seller=request.user,
                product_id=product_data["id"],
                size=product_data["size"],
                color=product_data["color"],
                quantity=product_data["quantity"],
                price=product_data["price"],
            )
            try:
                product_order.save()
                sell_order.add_product(product_order)
            except ValueError as e:
                error_message = str(e)
                response_data = {"error": error_message}
                return JsonResponse(response_data, status=400)
        sell_order.save()
        response_data = {"message": "Product orders created successfully","ordid":sell_order.id}
        return JsonResponse(response_data, status=200)

    return JsonResponse({}, status=405)