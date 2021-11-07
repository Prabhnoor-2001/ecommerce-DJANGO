from django.urls import path
from . import views

urlpatterns = [
    path('',views.ecommerce, name='ecommerce'),
    path('checkout/',views.checkout, name='checkout'),
    path('cart/',views.cart, name='cart'),
    path('updateItem/',views.updateItem, name='update'),
    path('processOrder/',views.processOrder, name='processOrder')
]