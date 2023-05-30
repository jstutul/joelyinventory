from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from authuser.views import admin_required
from django.contrib import messages

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
        status = request.POST.get('status')
        user_type = request.POST.get('user_type')
        
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
        if status==1:
            user.is_active=True
        else:
            user.is_active=False    

        if user_type==1:
            user.is_staff=True
            user.is_superuser=True
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