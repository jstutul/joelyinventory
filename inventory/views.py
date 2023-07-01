from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authuser.views import admin_required,staff_required
from django.contrib import messages
from django.core.paginator import Paginator
from inventory.models import Product,ProductReturn,Notifications
from .forms import ProductForm,ProductReturnForm,SellUpdateForm
from django.http import JsonResponse
from joelypos.utility import *
from pos.models import Sell,SellOrder
from datetime import datetime
from django.db.models import Sum,Avg,Count
from django.db import IntegrityError

def get_total_sell_amount():
    total_sell_amount = Sell.objects.aggregate(total_amount=Sum('order__total'))
    return total_sell_amount['total_amount']


@login_required(login_url='App_Auth:login')
@admin_required
def dashboard(request):
    total_peoduct=Product.objects.filter(status=True)
    total_cost = total_peoduct.aggregate(total_cost=Sum('totalcost'))['total_cost']
    total_sell=Sell.objects.all()
    product_stats = total_peoduct.aggregate(total_cost=Sum('totalcost'), total_products=Count('id'))
    total_cost = product_stats['total_cost']
    total_products = product_stats['total_products']

    if total_products > 0:
        average_cost = round(total_cost / total_products, 2)
    else:
        average_cost = 0.00
        
    average_order = SellOrder.objects.filter(is_payment=True).aggregate(average_total=Avg('total'))
    average_total = average_order['average_total']

    if average_total is not None:
        average_total = round(average_total, 2)
    else:
        average_total = 0.00    
    
    
    # Get the current year
    current_year = datetime.now().year
    average_order = Sell.objects.filter(status=True, created__year=current_year).aggregate(average_total=Avg('order__total'))
    average_total = average_order['average_total'] or 0.0  # Set default value to 0.0 if average_total is None
    average_total=round(average_total,2)
    
    context={
        'total_peoduct':total_peoduct.count(),
        'total_sell':total_sell.count(),
        'total_sell_amount':get_total_sell_amount(),
        'total_costing':total_cost,
        'average_cost':average_cost,
        'average_total':average_total,
    }
    return render(request,'inventory/index.html',context)


#get all user list
@login_required(login_url='App_Auth:login')
@admin_required
def userlist(request):
    
    search_name = request.GET.get('username', '')
    search_usertype = request.GET.get('usertype', '')
    search_status = request.GET.get('userstatus', '')
    users = User.objects.exclude(pk=request.user.pk)          

    if search_name:
        users=users.filter(username__icontains=search_name)
    if search_usertype:
        if search_usertype=="1":
            users=users.filter(is_superuser=True,is_staff=True)
        if search_usertype=="2":
            users=users.filter(is_staff=True , is_superuser=False)
        if search_usertype=="3":
            users=users.filter(is_active=True,is_staff=False)    
    if search_status:
        if search_status=="1":
            users=users.filter(is_active=True)
        if search_status=="2":
            users=users.filter(is_active=False) 
            

    paginator = Paginator(users, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'product_list': page_obj,
        'search_name': search_name,
        'search_status':search_status,
        'search_usertype':search_usertype,
    }
    return render(request,'inventory/users/users.html',context)


#add user page
@login_required(login_url='App_Auth:login')
@admin_required

def adduser(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        status = request.POST.get('my_userstatus')
        user_type = request.POST.get('my_usertype')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('App_inventory:adduser')
        if User.objects.filter(username=username).exists():
            messages.error(request,"username already exist try another one.")
            return redirect('App_inventory:adduser')
        
        user = User.objects.create_user(
            username=username, 
            password=password, 
            email=email,
        )
        user.first_name = first_name
        user.last_name = last_name
        if status=="1":
            user.is_active=True
        else:
            user.is_active=False 
               
        if user_type=="1":
            user.is_staff=True
            user.is_superuser=True
        elif user_type=="2":
            user.is_staff=True
            user.is_superuser=False
        else:
            user.is_staff=False
            user.is_superuser=False 
        user.save()
        messages.success(request,"you have successfully added new user")
        return redirect('App_inventory:adduser')
    else:
        return render(request,'inventory/users/addusers.html')

@login_required(login_url='App_Auth:login')
@admin_required    
def deleteuserdata(request):
    # try:
    if request.method=="POST":
        id=request.POST["userdeletemodal"]
        user = get_object_or_404(User, id=id)
        user.delete()
        messages.success(request,"user data deleted")
    else:
        messages.error(request,"something went wrong")          
    return redirect('App_inventory:userslist')    
    # except:
    #     messages.error(request,"something went wrong except")
    #     return redirect('App_inventory:userslist')   
    
#edit user page
@login_required(login_url='App_Auth:login')
@admin_required    
def edituserdata(request,id):
    # try:
        
    # except:
    #     user=None
    user=User.objects.get(id=id)
    if request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        status = request.POST.get('my_userstatus')
        user_type = request.POST.get('my_usertype')
        
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        if status=="1":
            user.is_active=True
        else:
            user.is_active=False 
               
        if user_type=="1":
            user.is_staff=True
            user.is_superuser=True
        elif user_type=="2":
            user.is_staff=True
            user.is_superuser=False
        else:
            user.is_staff=False
            user.is_superuser=False 
        user.save()    
        messages.success(request,"user update successfully")
        return redirect('App_inventory:userslist')   

    context={
        'user':user
    }
    return render(request,'inventory/users/edit.html',context)    


@login_required(login_url='App_Auth:login')
@staff_required  
def viewproduct(request):
    search_name = request.GET.get('productname', '')
    search_category = request.GET.get('productcategory', '')
    search_color = request.GET.get('productcolor', '')
    search_size = request.GET.get('productsize', '')
                   
    products = Product.objects.filter(
        status=True
    )
    
    if search_name:
        products=products.filter(name__icontains=search_name)
    if search_category:
        products=products.filter(category=search_category)
    if search_color:
        products=products.filter(color=search_color)
    if search_size:
        products=products.filter(size=search_size)            
    
    
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'product_list': page_obj,
        'search_name': search_name,
        'selected_category': search_category,
        'selected_color': search_color,
        'selected_size': search_size,
        'category_choices': Product.CATEGORY_CHOICES,
        'color_choices': Product.COLOR_CHOICES,
        'size_choices': Product.SIZE_CHOICES,
    }
    return render(request,'inventory/products/products.html',context)    
@login_required(login_url='App_Auth:login')
@staff_required 
def addproductview(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"product added successfully")
            return redirect('App_inventory:addproduct')
    else:
        form = ProductForm()
    context={
        'form':form,
    }    
    return render(request,'inventory/products/addproduct.html',context)

@login_required(login_url='App_Auth:login')
@staff_required 
def editproductview(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"product update successfully")
            return redirect(product.get_absolute_url())
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventory/products/editproduct.html', {'form': form})

@login_required(login_url='App_Auth:login')
@staff_required
def deleteproductview(request):
   
    if request.method == 'POST':
        id=request.POST.get("id")
        product = get_object_or_404(Product,id=id)
        if request.user.is_staff or request.user.is_superuser:
            product.status = False
            product.save()
            noti=Notifications.objects.create(
                user=request.user,
                message= "Hello Admin, ( "+str(request.user)+" ) user ,removed a product from product list."
            )
            noti.save()
            messages.success(request,"product removed successfully")
    else:        
        messages.error(request,"Somethig went wrong")
    return redirect('App_inventory:products')


@login_required(login_url='App_Auth:login')
@admin_required
def restoreviewproduct(request):
    search_name = request.GET.get('productname', '')
    search_category = request.GET.get('productcategory', '')
    search_color = request.GET.get('productcolor', '')
    search_size = request.GET.get('productsize', '')
                   
    products = Product.objects.filter(
        status=False
    )
    
    if search_name:
        products=products.filter(name__icontains=search_name)
    if search_category:
        products=products.filter(category=search_category)
    if search_color:
        products=products.filter(color=search_color)
    if search_size:
        products=products.filter(size=search_size)            
    
    
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'product_list': page_obj,
        'search_name': search_name,
        'selected_category': search_category,
        'selected_color': search_color,
        'selected_size': search_size,
        'category_choices': Product.CATEGORY_CHOICES,
        'color_choices': Product.COLOR_CHOICES,
        'size_choices': Product.SIZE_CHOICES,
    }
    return render(request,'inventory/remove/products.html',context)  

@login_required(login_url='App_Auth:login')
@admin_required
def restoreremovedproductview(request):
    if request.method == 'POST':
        id=request.POST.get("id")
        product = get_object_or_404(Product,id=id)
        product.status = True
        product.save()
        messages.success(request,"product restore successfully")
    else:        
        messages.error(request,"Somethig went wrong")
    return redirect('App_inventory:restoreproducts')


@login_required(login_url='App_Auth:login')
@admin_required
def deleteremovedproductview(request):
    try:
        if request.method == 'POST':
            id = request.POST.get("id")
            product = get_object_or_404(Product, id=id)
            print(product)
            product.delete()
            messages.success(request, "Product deleted successfully")
        else:        
            messages.error(request, "Something went wrong")
    except IntegrityError as e:
        messages.error(request, "Cannot delete the product due to existing references.")
        return redirect('App_inventory:restoreproducts')
    except Exception as ex:
        messages.error(request, "An error occurred while deleting the product.")
        return HttpResponse(str(ex))
    return redirect('App_inventory:restoreproducts')
    
@login_required(login_url='App_Auth:login')
@admin_required
def returnproductview(request):
    search_name = request.GET.get('productname', '')
    search_category = request.GET.get('productcategory', '')
    search_color = request.GET.get('productcolor', '')
    search_size = request.GET.get('productsize', '')
    products = ProductReturn.objects.all()              

    if search_name:
        products=products.filter(product__name__icontains=search_name)
    if search_category:
        products=products.filter(product__category=search_category)
    if search_color:
        products=products.filter(product__color=search_color)
    if search_size:
        products=products.filter(product__size=search_size)            
    
    
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'product_list': page_obj,
        'search_name': search_name,
        'selected_category': search_category,
        'selected_color': search_color,
        'selected_size': search_size,
        'category_choices': Product.CATEGORY_CHOICES,
        'color_choices': Product.COLOR_CHOICES,
        'size_choices': Product.SIZE_CHOICES,
    }
    return render(request, 'inventory/returnproduct/products.html', context)

@login_required(login_url='App_Auth:login')
@staff_required
def addreturnproduct(request):
    if request.method == 'POST':
        form = ProductReturnForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            addedby = request.user
            
            product_obj = get_object_or_404(Product, id=product.id)
            
            existing_return = ProductReturn.objects.filter(product=product, addedby=addedby).first()
            
            if product_obj.quantity < quantity :
                messages.error(request,"you cann't return more then available product.")
                return redirect('App_inventory:addreturnproduct')
            if existing_return:
                existing_return.quantity += quantity
                existing_return.save()
                messages.success(request,"Return product updated.")
            else:
                new_return = form.save(commit=False)
                new_return.addedby = addedby
                new_return.save()
                messages.success(request,"New product added to return list.")
                
            product_obj.quantity =product_obj.quantity-quantity
            product_obj.save()    
            return redirect('App_inventory:addreturnproduct')
    else:
        form = ProductReturnForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inventory/returnproduct/addproduct.html', context)


@login_required(login_url='App_Auth:login')
@admin_required
def editreturnproduct(request,id):
    product_return = get_object_or_404(ProductReturn, id=id)
    if request.method == 'POST':
        form = ProductReturnForm(request.POST, instance=product_return)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            old_quantity = request.POST['oldq']
            newQuantity=int(old_quantity)-int(product_return.quantity)
            existing_return = Product.objects.get(id=product_return.product.id)
            if int(existing_return.quantity) > int(newQuantity):
                existing_return.quantity=existing_return.quantity +(newQuantity)
                existing_return.save()
                form.save()
                messages.success(request,"Prodcut info updated successfully.")
            else:
                messages.error(request,"Prodcut quantity can not me less then zero.")
            return redirect(product_return.get_absolute_url())  
    else:
        form = ProductReturnForm(instance=product_return)
    
    return render(request, 'inventory/returnproduct/editproduct.html', {'form': form})



@login_required(login_url='App_Auth:login')
@admin_required
def getproductquantity(request):
    product_id = request.GET.get('id')
    try:
        product = get_object_or_404(Product, id=product_id)
        data = {
            'quantity': product.quantity,
        }
    except:
        data={}
    return JsonResponse(data)

@login_required(login_url='App_Auth:login')
@staff_required
def barcodeview(request):
    product=Product.objects.filter(status=True)
    context={
        'products':product,
    }
    return render(request, 'inventory/barcode/index.html',context)

@login_required(login_url='App_Auth:login')
@staff_required
def getbarcodeimage(request):
    product_id = request.GET.get('id')
    try:
        product = get_object_or_404(Product, id=product_id)
        data = {
            'pid': product.id,
            'barcode': "/"+str(product.barcode).replace("\\","/"),
        }
    except:
        data={}
    return JsonResponse(data)

@login_required(login_url='App_Auth:login')
@staff_required
def Saleview(request):
    payment_status = request.GET.get('payment_status', '')
    start_date     = request.GET.get('start_date', '')
    end_date       = request.GET.get('end_date', '')
    
    std=start_date
    etd=end_date
    products = Sell.objects.filter(status=True)

    if payment_status:
        products = products.filter(paymentstatus=payment_status)

    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        products = products.filter(created__date__gte=start_date)
    if end_date:    
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        products = products.filter(created__date__lte=end_date)

    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'product_list': page_obj,
        'payment_status': payment_status,
        'paymentstatus_choices': Sell.PAYMENT_STATUS,
        'start_date': std,
        'end_date': etd,
    }
    return render(request,'inventory/sales/index.html',context)

@login_required(login_url='App_Auth:login')
@staff_required
def SaleDetailsview(request, id):
    try:
        order = get_object_or_404(Sell, id=id)
    except Sell.DoesNotExist:
        order = None   
    context = {
        "order": order,
    }
    return render(request, 'inventory/sales/saledetails.html', context)

@login_required(login_url='App_Auth:login')
@staff_required
def SalesEditview(request,id):
    try:
        sell = Sell.objects.get(id=id)
        if request.method == 'POST':
            form = SellUpdateForm(request.POST, instance=sell)
            if form.is_valid():
                form.save()
                messages.success(request, 'Sell data updated successfully.')
                return redirect('App_inventory:sale')
        else:
            form = SellUpdateForm(instance=sell)
    except:
        sell={}        
    return render(request, 'inventory/sales/saleedit.html', {'form': form})


#notification
def NotificationView(request):
    try:
        noti=Notifications.objects.all()
    except:
        return redirect('App_inventory:dashboard')
    
    context={
        'notification':noti,
    }
    return render(request,'inventory/notification/index.html',context)


def NotificationDeleteView(request,id):
    try:
        noti=get_object_or_404(Notifications,id=id)
        noti.delete()
        messages.success(request,'notification deleted')
    except:
        messages.info(request,'someting went wrong')
    return redirect('App_inventory:notifications')
    