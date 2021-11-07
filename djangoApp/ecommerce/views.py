from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime

# Create your views here.
def ecommerce(request):
    viewData = {'products':Product.objects.all()}
    return render(request, 'ecommerce/ecommerce.html', viewData)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)#created is a bool 
        items = order.orderitem_set.all()
    else:
        items =[]
        order={'getCartTotal':0,'getCartItems':0, 'shipping': False}

    viewData = {'items':items, 'order':order}
    return render(request, 'ecommerce/cart.html', viewData)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)#created is a bool 
        items = order.orderitem_set.all()
    else:
        items =[]
        order={'getCartTotal':0,'getCartItems':0, 'shipping': False}

    viewData = {'items':items, 'order':order}
    return render(request, 'ecommerce/checkout.html', viewData)

def updateItem(request):
    data = json.loads(request.body)
    product = data['product']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=product)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity +=1
    elif action =='remove':
        orderItem.quantity -=1

    orderItem.save()
    if orderItem.quantity <=0 :
        orderItem.delete()

    return JsonResponse('product', safe=False)
    
def processOrder(request):
    transactionId = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)#created is a bool 
        total = float(data['userForm']['total'])
        order.transaction_id = transactionId 

        if total == order.getCartTotal:
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shippingInfo']['address'],
                city=data['shippingInfo']['city'],
                state=data['shippingInfo']['state'],
                zipcode=data['shippingInfo']['zipcode'],
                

            )
    return JsonResponse('completed',safe=False)