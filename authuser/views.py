from django.shortcuts import render,redirect
from django.contrib import messages,auth
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from functools import wraps
import requests


def authenticated_user(view_func) :
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.session.get('user').get('is_authenticated') :
            return view_func(request, *args, **kwargs)
        else :
            return redirect('App_Auth:login')
    return wrapper_func


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            return render(request,'authuser/accessdenied.html')
        return view_func(request, *args, **kwargs)
    return wrapper


def loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,"you are now authenticated")
            url=request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params=dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except Exception:
                return redirect('App_inventory:dashboard')
        else:
            messages.error(request, "invalid credential")
            return redirect('App_Auth:login')
    context={}
    return render(request,'authuser/login.html')

def logoutview(request):
    auth.logout(request)
    messages.success(request, "Successfully Logout")
    return redirect('App_Auth:login')