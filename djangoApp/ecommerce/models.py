from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey
import sys

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=254, null=True)
    email = models.EmailField(max_length=254)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=254)
    price = models.FloatField()
    digital = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id  = models.CharField(max_length=128, null=True)

    def __str__(self) -> str:
        return str(self.id)

    @property
    def getCartTotal(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.getTotal for item in orderItems])
        return total
    @property
    def getCartItems(self):
        orderItems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderItems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,null=True)
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=254, null=False)
    city = models.CharField(max_length=254, null=False)
    state = models.CharField(max_length=254, null=False)
    zipcode = models.CharField(max_length=254, null=False)

    def __str__(self) -> str:
        return self.address