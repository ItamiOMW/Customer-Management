from django.forms import inlineformset_factory
from django.shortcuts import render, redirect

from .forms import OrderForm
from .models import *


# Create your views here.
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


def products(request):
    list_products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': list_products})


def customer(request, primary_key):
    customer_entity = Customer.objects.get(id=primary_key)

    orders = customer_entity.order_set.all()
    orders_count = orders.count()

    context = {'customer': customer_entity, 'orders': orders, 'orders_count': orders_count}
    return render(request, 'accounts/customer.html', context)


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


def delete_order(request, primary_key):
    order = Order.objects.get(id=primary_key)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}

    return render(request, 'accounts/delete.html', context)
