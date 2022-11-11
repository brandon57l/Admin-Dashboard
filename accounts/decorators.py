from django.http import HttpResponse
from django.shortcuts import redirect

def login_check(view):
    def check(request, *args, **kwargs ):
        if request.user.is_authenticated:
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group=='admin':
                    return redirect('home')
                elif group=='customer':
                    return redirect('user_page')
        else:
            return view(request, *args, **kwargs )
    return check

def access_authorization(groups_allowed=[]):
    def decorator(view):
        def check(request, *args, **kwargs ):
                
                group = None

                if request.user.groups.exists():
                    group = request.user.groups.all()[0].name

                if group in groups_allowed:
                    return view(request, *args, **kwargs )
                else:
                    return HttpResponse('You are not authorized to access this page.')

        return check
    return decorator

def admin_only(view):
    def check(request, *args, **kwargs):
        if request.user.groups.exists():
            group =  request.user.groups.all()[0].name
            if group=='admin':
                return view(request, *args, **kwargs)
            else:
                return redirect('user_page')
    return check