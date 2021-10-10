from django.db import models
from authy.models import User, Address
from .product import Product
import uuid


STATUS = (
    ('1', 'Order Placed'),
    ('2', 'Packed'),
    ('3', 'Shipped'),
    ('4', 'Out for delivery'),
    ('5', 'Delivered'),
    ('404','Cancelled')
)


class Order(models.Model):
    id=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='deliveryAddress')
    timestamp = models.DateTimeField(auto_now_add=True)
    actualAmt=models.FloatField(default=0.0)
    amt = models.FloatField(default=0.0)
    saved = models.FloatField(default=0.0)
    status = models.CharField(max_length=100, choices=STATUS)
    active = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_item")
    amt = models.FloatField()
    status=models.CharField(max_length=100, choices=STATUS)
    expectedDelivery=models.DateField(blank=True, default="2099-05-31")



class Payment(models.Model):
    order = models.ForeignKey(Order, related_name='payment', on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, default="")
    razorpay_order_id = models.CharField(max_length=100, default="")
    successful = models.BooleanField(default=False)
    refund=models.BooleanField(default=False)


class Refund(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE, related_name='refund')
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE,related_name='refundPayment')
    refund_id=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)