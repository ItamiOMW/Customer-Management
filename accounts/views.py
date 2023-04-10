from django.shortcuts import render

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


def customer(request):
    return render(request, 'accounts/customer.html')
