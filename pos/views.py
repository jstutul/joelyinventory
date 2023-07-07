import math 
import json
from django.contrib import messages
from pos.models import ProductOrder
from django.core import serializers
from django.http import JsonResponse
from inventory.models import Product
from pos.models import SellOrder,Sell,SalesReturn
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse

# Create your views here.

@login_required(login_url='App_Auth:login')
def poshome(request):
    context = {
        'category_choices': Product.CATEGORY_CHOICES,
        'color_choices': Product.COLOR_CHOICES,
        'size_choices': Product.SIZE_CHOICES,
    }
    return render(request,'pos/pos/index.html',context)
import uuid
@login_required(login_url='App_Auth:login')
def get_product_api(request):
    barcode = request.GET.get('barcode')
    category = request.GET.get('category')
    color = request.GET.get('color')
    size = request.GET.get('size')
    print(category,color,size,barcode)
    products = Product.objects.all()
    if barcode:
        products = products.filter(qcode=barcode)
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
            order.is_payment=True
            for ord in order.product.all():
                ord.order=True
                ord.product.quantity=int(ord.product.quantity)-int(ord.quantity)
                ord.save()
            order.save()
            messages.success(request,"Order Completed")
            return redirect('App_pos:poshome')
            
    except:
        return HttpResponse("<h1>Something Went Wrong</h1>")
    
    context={
        'order':order,
        'status': Sell.PAYMENT_STATUS,
    }
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
#sales return api

def salesreturnview(request):
    try:
        invoice_no = request.GET.get('invoice_no', '')
        sell=None
        product_data = []
        if invoice_no:
            sell = get_object_or_404(Sell, id=invoice_no)
            product_orders = sell.order.product.all()
            for product_order in product_orders:
                product_data.append({
                    'product':product_order.product,
                    'product_name': product_order.product.name,
                    'quantity': product_order.quantity,
                    'sell_price': product_order.price
                })    
    except:
        return HttpResponse("<h1>Something Went Wrong</h1>")  
    context={
        'selldata':sell,
        'invoice_no':invoice_no,
        'product_data':product_data,
    }    
    return render(request,'pos/salesreturn/salesreturn.html',context)


@csrf_exempt
# def save_sales_return(request):
    
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         sell_id = data.get('sid', 0)
#         sellproduct = data.get('sellproduct', [])
        
#         sell_data = Sell.objects.get(id=sell_id)
#         order_list = sell_data.order.product.filter(product__id__in=sellproduct)
        
#         subtotal = 0
#         for order in order_list:
#             subtotal += order.quantity*order.price
#             order.product.quantity += order.quantity
#             order.product.save()
#             order.delete()
        
#         sell_data.order.subtotal -= subtotal
#         sell_data.order.total = sell_data.order.subtotal - sell_data.order.discount
#         sell_data.order.save()
#         return JsonResponse({}, status=200)
#     else:
#         return JsonResponse({}, status=400)
    
  
def save_sales_return(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        sell_id = data.get('sid', 0)
        sellproduct = data.get('sellproduct', [])
        
        sell_data = Sell.objects.get(id=sell_id)
        
        subtotal = 0
        for item in sellproduct:
            pid = item.get('pid', 0)
            quantity = int(item.get('q', 1))
            
            # try:
            order = sell_data.order.product.get(product__id=pid)
            product = order.product
            
            if quantity >= product.quantity:
                # Remove the product from the order and delete it
                subtotal += order.quantity * order.price
                # product.quantity = 0
                # product.save()
                order.delete()
            else:
                # Decrease the quantity of the product in the order
                subtotal += quantity * order.price
                product.quantity += quantity
                product.save()
                order.quantity -= quantity
                order.save()
                
                if order.quantity <= 0:
                    order.delete()
                # Insert or update SalesReturn
                # Insert or update SalesReturn
                sales_return, _ = SalesReturn.objects.get_or_create(
                    user=request.user,
                    prodcut=order,
                    defaults={
                        'quantity': quantity,
                        'customer': sell_data.customer,
                        'mobile': sell_data.phone
                    }
                )
                if not _:
                    sales_return.quantity += quantity
                    sales_return.save()    
            # ecept Order.DoesNotExist:
            #     pass
        
        sell_data.order.subtotal -= subtotal
        sell_data.order.total = sell_data.order.subtotal - sell_data.order.discount
        sell_data.order.save()
        
        return JsonResponse({}, status=200)
    else:
        return JsonResponse({}, status=400)