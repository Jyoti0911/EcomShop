from django.urls import path, include
from . import views

urlpatterns = [
    
    path('',views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'),
    path('checkout/',views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]