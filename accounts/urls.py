from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user, name='logout'),

    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('customer/<str:id>/', views.customer, name='customer'),
    path('user_page/', views.user_page, name='user_page'),
    
    path('create_order/', views.create_order, name='create_order'),    
    path('update_order/<str:id>/', views.update_order, name='update_order'),
    path('delete_order/<str:id>/', views.delete_order, name='delete_order'),

    path('create_customer/', views.create_customer, name='create_customer'),
    path('update_customer/<str:id>/', views.update_customer, name='update_customer'),
    path('delete_customer/<str:id>/', views.delete_customer, name='delete_customer'),
    
   
]