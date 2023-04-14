from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .decorators import unauthenticated_user, allowed_users, admin_only
from .filters import OrderFilter
from .forms import OrderForm, CreateUserForm, CustomerForm
from .models import *


@unauthenticated_user
def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user_entity = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user_entity.groups.add(group)

            Customer.objects.create(
                user=user_entity,
                name=username
            )

            messages.success(request, f"User {username} registered successfully")
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_entity = authenticate(request, username=username, password=password)

        if user_entity is not None:
            login(request, user_entity)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    list_orders = Order.objects.all()
    list_customers = Customer.objects.all()
    orders_count = list_orders.count()
    orders_delivered = list_orders.filter(status="Delivered").count()
    orders_pending = list_orders.filter(status="Pending").count()
    customers_count = list_orders.count()

    context = {'orders': list_orders,
               'customers': list_customers,
               'orders_count': orders_count,
               'orders_delivered': orders_delivered,
               'customers_count': customers_count,
               'orders_pending': orders_pending
               }

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def account_settings(request):
    customer_entity = request.user.customer
    form = CustomerForm(instance=customer_entity)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer_entity)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    list_products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': list_products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, primary_key):
    customer_entity = Customer.objects.get(id=primary_key)

    orders = customer_entity.order_set.all()
    orders_count = orders.count()

    order_filter = OrderFilter(request.GET, queryset=orders)
    orders = order_filter.qs

    context = {
        'customer': customer_entity,
        'orders': orders,
        'orders_count': orders_count,
        'order_filter': order_filter
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, primary_key):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)

    customer_entity = Customer.objects.get(id=primary_key)
    form_set = OrderFormSet(queryset=Order.objects.none(), instance=customer_entity)

    if request.method == 'POST':
        form_set = OrderFormSet(request.POST, instance=customer_entity)
        if form_set.is_valid():
            form_set.save()
            return redirect('/')

    context = {'form': form_set}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, primary_key):
    order = Order.objects.get(id=primary_key)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, primary_key):
    order = Order.objects.get(id=primary_key)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}

    return render(request, 'accounts/delete.html', context)
