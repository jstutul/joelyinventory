from django.shortcuts import render
from functools import wraps
from django.contrib.auth.models import User

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request,'inventory/accessdenied.html')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def dashboard(request):
    return render(request,'inventory/index.html')


@admin_required
def userlist(request):
    # Retrieve all users except the logged-in user
    users = User.objects.exclude(pk=request.user.pk)
    #make dict to pass data to template
    context={
        'user_list':users,
    }
    return render(request,'inventory/users/users.html',context)


@admin_required
def adduser(request):
    return render(request,'inventory/users/addusers.html')