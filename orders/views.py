import re
from django.shortcuts import render , redirect
from django.contrib import messages
from products.models import Product
from orders.models import Order , OrderDetails
from django.utils import timezone
from .models import Payment

# Create your views here.
def add_to_card(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous:
        
        pro_id = request.GET['pro_id']
        qty = request.GET['qty']

        order = Order.objects.all().filter(user = request.user , is_finished = False)

        if not Product.objects.all().filter(id = pro_id).exists():
            return redirect('products')

        pro = Product.objects.get(id = pro_id)

        if order:
            old_order = Order.objects.get(user = request.user, is_finished = False)
            if OrderDetails.objects.all().filter(order = old_order, product = pro).exists():
                order_details = OrderDetails.objects.get(order = old_order , product = pro)
                order_details.quantity += int(qty)
                order_details.save()
            else:
                order_details = OrderDetails.objects.create(
                    order = old_order,
                    product = pro,
                    price = pro.price,
                    quantity = qty
                )
            messages.success(request , 'has added to card for old order')
        else:
            new_order = Order()
            new_order.user = request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            order_details = OrderDetails.objects.create(
                order = new_order,
                product = pro,
                price = pro.price,
                quantity = qty
            )
            messages.success(request , 'has added to card for new order')

        return redirect('/products/' + request.GET['pro_id'])
    else:
        #return redirect('products')
        if 'pro_id' in request.GET:
            messages.error(request, 'you must be logged in')
            return redirect('/products/' + request.GET['pro_id'])
        else:
            return redirect('index')

def card(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        if Order.objects.all().filter(user = request.user , is_finished = False):
            order = Order.objects.get(user = request.user , is_finished = False)
            order_details = OrderDetails.objects.all().filter(order = order)
            total = 0
            for sub in order_details:
                total += sub.price*sub.quantity
            context = {
                'order': order,
                'order_details': order_details,
                'total': total
            }
    return render(request , 'orders/card.html' , context)

def remove_from_card(request , order_details_id):
    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            order_details.delete()
    return redirect('card')

def add_qty(request , order_details_id):

    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            order_details.quantity +=1 
            order_details.save()

    return redirect('card')
def sub_qty(request , order_details_id):

    if request.user.is_authenticated and not request.user.is_anonymous and order_details_id:
        order_details = OrderDetails.objects.get(id = order_details_id)
        if order_details.order.user.id == request.user.id:
            if order_details.quantity > 1:
                order_details.quantity -=1 
                order_details.save()
    
    return redirect('card')

def payment(request):
    context = None
    ship_address = None
    ship_phone = None
    card_number = None
    expire = None
    security_code = None
    is_added = None

    if request.method == 'POST' and ('btn_payment' and 'ship_address' and 'ship_phone' and 'card_number' and 'expire' and 'security_code' ) in request.POST:
        #payment operation after click on button
        ship_address = request.POST['ship_address']
        ship_phone = request.POST['ship_phone']
        card_number = request.POST['card_number']
        expire = request.POST['expire']
        security_code = request.POST['security_code']

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user , is_finished = False):
                order = Order.objects.get(user = request.user , is_finished = False)

                payment = Payment(
                    order = order ,
                    shipment_address = ship_address,
                    shipment_phone = ship_phone,
                    card_number = card_number,
                    expire = expire,
                    security_code = security_code     
                )
                payment.save()
                order.is_finished = True
                order.save()
                is_added = True
                messages.success(request , 'your order is finished')

        context = {
            'ship_address': ship_address,
            'ship_phone': ship_phone,
            'card_number': card_number,
            'expire': expire,
            'security_code': security_code,
            'is_added': is_added,
        }
    else:
        #shown Before click on button
        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.all().filter(user = request.user , is_finished = False):
                order = Order.objects.get(user = request.user , is_finished = False)
                order_details = OrderDetails.objects.all().filter(order = order)
                total = 0
                for sub in order_details:
                    total += sub.price*sub.quantity
                context = {
                    'order': order,
                    'order_details': order_details,
                    'total': total
                }
    return render(request , 'orders/payment.html', context)

def show_orders(request):
    context = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user = request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id = x.id)
                order_details = OrderDetails.objects.all().filter(order = order)
                total = 0
                for sub in order_details:
                    total += sub.price*sub.quantity
                x.total = total
                x.items_count = order_details.count
    context = {
        'all_orders': all_orders
    }
    return render(request , 'orders/show_orders.html', context)