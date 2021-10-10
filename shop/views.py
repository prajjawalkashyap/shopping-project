from shop.shopModels.product import Category, SubCategory
from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem, OrderProduct, Order, Payment, Review, Wishlist, ProductMedia, Coupon, \
    CouponUsed
#from authy.models import User, Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# =========== SHOP HOME ==================
def shop(request):
    product = Product.objects.all()
    category=Category.objects.all()
    sub=SubCategory.objects.all()
    context={
        'products': product,
        'category':category,
        'subcategory':sub
    }
    return render(request, 'shop/home.html',context)
# ============ END SECTION ====================
