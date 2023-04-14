from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.registerUser, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
        name='reset_password'
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
        name='password_reset_confirm'
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_done.html'),
        name='password_reset_confirm'
    ),

    path('', views.home, name="home"),
    path('user/', views.user, name='user'),
    path('settings/', views.account_settings, name='account'),

    path('products/', views.products, name="products"),
    path('customer/<str:primary_key>/', views.customer, name="customer"),

    path('create_order/<str:primary_key>/', views.create_order, name="create_order"),
    path('update_order/<str:primary_key>/', views.update_order, name="update_order"),
    path('delete_order/<str:primary_key>/', views.delete_order, name="delete_order"),
]
