from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authuser.views import admin_required,staff_required
from django.contrib import messages
from inventory.models import Product
from .forms import CategoryForm, ProductForm


@login_required(login_url='App_Auth:login')
@admin_required
def dashboard(request):
    return render(request,'inventory/index.html')


#get all user list
@login_required(login_url='App_Auth:login')
@admin_required
def userlist(request):
    # Retrieve all users except the logged-in user
    users = User.objects.exclude(pk=request.user.pk)
    #make dict to pass data to template
    context={
        'user_list':users,
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
        
        print(user,status,user_type)
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
    products = Product.objects.filter(status=True)
    context={
        'product_list':products,
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
        if request.user.is_superuser:
            product.delete()
        elif request.user.is_staff:
            product.status = False
            product.save()
            messages.success(request,"product update successfully")
    else:        
        messages.error(request,"Somethig went wrong")
    return redirect('App_inventory:products')
