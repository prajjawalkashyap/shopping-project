from django.core.checks import messages
from shop.models import Product, Cart, CartItem, OrderProduct, Order, Payment, Review, Wishlist, ProductMedia, Coupon, \
    CouponUsed
from django.http import JsonResponse
import json
from authy.models import User, Address
from shop.context_processors import cartProcessor
from django.contrib.auth.decorators import login_required


# ============ COUPON CODE CHECKING=====================
def couponCheck(request):
    data = json.loads(request.body)
    coupon = data['coupon']
    try:
        coup = Coupon.objects.get(code=coupon)
        coupUsed=CouponUsed.objects.filter(coupon=coup, user=request.user)
        if coupUsed:
            context={
                'message': 'Coupon already used',
                'error': 'Error'
            }
        else:
            cart = cartProcessor(request)

            cartTotal = cart['cartTotal']

            if cartTotal >= coup.condition:
                cartTotal -= coup.discount
                context = {
                    'error': 'None',
                    'message': 'Coupon applied',
                    'cartTotal': cartTotal,
                    'saving': coup.discount,
                    'code': coup.code
                }
            else:
                context = {
                    'message': 'Cart value >= ' + str(coup.condition),
                    'error': 'Error'
                }
    except Exception as e:
        print(e)
        context = {
            'message': 'Incorrect coupon code',
            'error': 'Error'
        }
    return JsonResponse(context)
# ============ END SECTION ====================
# =========MOVE TO CART===============
def moveToCart(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    if not action == "delete":
        cart = Cart.objects.get(user=request.user)
        cartItem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartItem.quantity = (cartItem.quantity + 1)
        amt = cartItem.product.price * cartItem.quantity
        cartItem.amt = amt
        cartItem.save()
        context = {
            'message': 'Removed from Wishlist and added to Cart'
        }
    else:
        context = {
            'message': 'Removed from Wishlist'
        }
    wish = Wishlist.objects.get(product=product)
    wish.delete()
    return JsonResponse(context)
# ============ END SECTION ====================
# ==========UPDATE WISHLIST==========
@login_required
def wishlist(request):
    context = {}
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    product = Product.objects.get(id=productId)
    if Wishlist.objects.filter(product=product,user=request.user) and action!='remove':
        context={
            'message':'Already in Wishlist'
        }
    else:
        if action == 'add':
            wish = Wishlist(user=request.user, product=product)
            wish.save()
            context = {
                'message': 'Added to Wishlist'
            }
        elif action == 'remove':
            wish = Wishlist.objects.get(product=product, user=request.user)
            wish.delete()
            context = {
                'message': 'Removed from Wishlist'
            }
    return JsonResponse(context)

# ============ END SECTION ====================
# ============UPDATE CART============
@login_required
def updateItem(request):
    cartPro = cartProcessor(request)

    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    product = Product.objects.get(id=productId)
    cartObj, created = Cart.objects.get_or_create(user=request.user)

    cartItem, created = CartItem.objects.get_or_create(cart=cartObj, product=product)

    if action == 'add':
        cartItem.quantity = (cartItem.quantity + 1)
    elif action == 'remove':
        cartItem.quantity = (cartItem.quantity - 1)

    amt = cartItem.product.price * cartItem.quantity
    cartItem.amt = amt
    cartItem.save()
    quant = cartItem.quantity
    if cartItem.quantity <= 0 or action == 'delete':
        cartItem.delete()

    cartItems = {
        'productId': cartItem.product.id,
        'quantity': quant,
        'amt': cartItem.amt,
        'cartTotal': cartPro['cartTotal'],
        'cartCount': cartPro['cartCount'],

        'productPrice': product.price
    }
    return JsonResponse(cartItems)
# ============ END SECTION ====================
