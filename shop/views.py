from django.shortcuts import render, redirect
from .models import Product, Order
from django.core.paginator import Paginator
from django.urls import reverse
import json
from decimal import Decimal, InvalidOperation

# Create your views here.
def index(request):
    product_objects=Product.objects.all()

    #search code
    item_name = request.GET.get('item_name')
    if item_name !='' and item_name is not None:
        product_objects=product_objects.filter(title__icontains=item_name)

    #paginator code
    paginator = Paginator(product_objects,4)
    page=request.GET.get('page')
    product_objects = paginator.get_page(page)    
    return render(request,'shop/index.html', {'product_objects':product_objects})

def detail(request,id):
    product_object=Product.objects.get(id=id)
    return render(request, 'shop/detail.html', {'product_object':product_object})

def checkout(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        city = request.POST.get('city', '')
        zipcode = request.POST.get('zipcode', '')

        # Safely get cart data
        cart_data = request.POST.get('cart_data', '{}')
        try:
            cart = json.loads(cart_data)
        except json.JSONDecodeError:
            cart = {}

        # Safely convert total price
        total_price_str = request.POST.get('total_price', '0').strip()

        # If empty or invalid, default to 0
        try:
            total_price = Decimal(total_price_str)
        except (InvalidOperation, TypeError, ValueError):
            total_price = Decimal('0.00')

        # ✅ Save order safely
        order = Order.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zipcode=zipcode,
            cart_data=cart,
            total_price=total_price
        )

        # ✅ Redirect to success page with ID
        return redirect(reverse('order_success', kwargs={'order_id': order.id}))

    return render(request, 'shop/checkout.html')

def order_success(request, order_id):
    """Success page after placing an order"""
    order = Order.objects.get(id=order_id)
    return render(request, 'shop/order_success.html', {'order': order})