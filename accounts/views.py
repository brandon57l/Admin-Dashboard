from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.decorators import login_required

from .decorators import *
from .models import *
from .forms import *
from .filters import *

# Create your views here.

@login_check
def register(request):

    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}.')
            return redirect('login')
        
    data = {'form':form}
    return render(request, 'register.html', data)

@login_check
def login_page(request):

    data = {}

    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)

            if user.groups.exists():
                group = user.groups.all()[0].name
                if group=='admin':
                    return redirect('home')
                elif group=='customer':
                    return redirect('user_page')
        else:
            messages.info(request, 'Username or password is incorrect.')

    return render(request, 'login.html', data)

def logout_user(request):
    logout(request)
    return redirect('login')

# @access_authorization(['admin'])
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_orders = orders.count()
    total_customers = customers.count()

    orders_delivered = orders.filter(status="Delivered").count()
    orders_pending = orders.filter(status="Pending").count()

    data = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'orders_delivered':orders_delivered, 'orders_pending':orders_pending}
    
    return render(request, 'dashboard.html', data)

@access_authorization(['admin','customer'])
def user_page(request):
    data = {}
    return render(request, 'user.html', data)

@access_authorization(['admin'])
def products(request):
    products = Product.objects.all()
    data = {'products':products}
    return render(request, 'products.html', data)

@access_authorization(['admin'])
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    total_orders = orders.count()
    
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs
    data = {'customer':customer, 'orders':orders, 'total_orders':total_orders, 'filter':filter}

    return render(request, 'customer.html', data)

@access_authorization(['admin'])
def create_customer(request):
    data = {'form':CustomerForm()}

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'customer_form.html', data)

@access_authorization(['admin'])
def update_customer(request, id):
    customer = Customer.objects.get(id=id)
    data = {'form':CustomerForm(instance=customer)}

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'customer_form.html', data)

@access_authorization(['admin'])
def delete_customer(request, id):
    customer = Customer.objects.get(id=id)
    data = {'customer':customer}

    if request.method=='POST':
        customer.delete()
        return redirect('/')

    return render(request, 'delete_customer.html', data)

@access_authorization(['admin'])
def create_order(request):
    data = {'form':OrderForm()}

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'order_form.html', data)

@access_authorization(['admin'])
def update_order(request, id):
    order = Order.objects.get(id=id)
    data = {'form':OrderForm(instance=order)}

    if request.method=='POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    return render(request, 'order_form.html', data)

@access_authorization(['admin'])
def delete_order(request, id):
    order = Order.objects.get(id=id)
    data = {'order':order}

    if request.method=='POST':
        order.delete()
        return redirect('/')
    
    return render(request, 'delete_order.html', data)
