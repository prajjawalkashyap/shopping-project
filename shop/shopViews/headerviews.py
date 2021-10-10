from django.shortcuts import render, redirect
from shop.models import Product, Cart, CartItem, OrderProduct, Order, Payment, Review, Wishlist, ProductMedia, Coupon, \
    CouponUsed
from authy.models import User, Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# =========== MY ORDER VIEW ===========
def myOrder(request):
    if request.user.is_authenticated:
        cd = {}
        orders = Order.objects.filter(user=request.user, active=True).order_by('-timestamp')
        for order in orders:
            payment=Payment.objects.get(order=order)
            items = OrderProduct.objects.filter(order=order)
            cd[order.id] = {
                'order': order,
                'items': items,
                'payment':payment
            }
        return render(request, 'shop/orderList.html', {'orders': cd})
# ============ END SECTION ====================
# ============= WISHLIST VIEW ===============
def wishlistView(request):
    if request.user.is_authenticated:
        wish = Wishlist.objects.filter(user=request.user)
        return render(request, 'shop/wishlist.html', {'wishlist': wish})
    else:
        messages.error(request, 'Login required')
        return redirect('/auth/login/')
# ============ END SECTION =======================
# ============== CART VIEW =======================
def cartView(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        cartItem = CartItem.objects.filter(cart=cart)
        total = 0.0
        for item in cartItem:
            total += item.amt
        context = {
            'items': cartItem,
            'total': total
        }
        return render(request, 'shop/cart.html', context)
    else:
        messages.error(request, 'Login to add to Cart')
        return redirect('/auth/login/')
# ============ END SECTION ====================
