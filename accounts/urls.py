from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('products/', views.products, name="products"),
    path('customer/<str:primary_key>/', views.customer, name="customer"),

    path('create_order/', views.create_order, name="create_order"),
    path('update_order/<str:primary_key>/', views.update_order, name="update_order"),
    path('delete_order/<str:primary_key>/', views.delete_order, name="delete_order")
]
