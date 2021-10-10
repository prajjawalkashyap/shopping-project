from django.db import models
from authy.models import User
from .product import Category, Product, SubCategory
from .payment import Order


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    total= models.FloatField(default=0.0)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartItem', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cartItem")
    quantity = models.IntegerField(default=0)
    amt = models.FloatField(default=0)
    timestamp=models.DateTimeField(auto_now_add=True)


class Coupon(models.Model):
    COUP_TYPE=(
        ('Discount','Discount'), 
        ('Cashback','Cashback')
        )
    code = models.CharField(max_length=100)
    type=models.CharField(max_length=50, choices=COUP_TYPE)
    discount = models.IntegerField()
    condition = models.IntegerField()
    desc=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    expiry = models.DateTimeField()
    expired=models.BooleanField(default=False)

    def __str__(self):
        return self.code
        


class CouponUsed(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='couponUsed')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='couponUser')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='couponOrder')


class Wishlist(models.Model):
    user = models.ForeignKey(User, related_name="wishlistUser", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="wishlistProduct", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Banner(models.Model):
    TYPE=(
        ('small','small'),
        ('medium','medium'),
        ('large','large')
    )
    type=models.CharField(max_length=10,choices=TYPE)
    text=models.TextField()
    image=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE, related_name="banner")
    subCategory=models.ForeignKey(SubCategory,on_delete=models.CASCADE, related_name="banner", blank=True)
    discount=models.FloatField(blank=True)
    coupon=models.ForeignKey(Coupon, on_delete=models.CASCADE, blank=True, related_name='banner')

