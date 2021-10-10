from django.shortcuts import render, redirect
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product, Cart, CartItem, OrderProduct, Order, Payment, Refund, Coupon, \
    CouponUsed
from authy.models import User, Address
from django.contrib import messages

from django.contrib.auth.decorators import login_required


# ==============CART CHECKOUT==============
def checkout(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartItem = CartItem.objects.filter(cart=cart)
        if cartItem:
            amt = 0
            for its in cartItem:
                amt += (its.product.price * its.quantity)

            address = Address.objects.filter(user=request.user)
            amount = amt * 100

            context = {
                'total_amt': amt,
                'cartItems': cartItem,
                'amount': amount,
                'addresses': address,

            }
            return render(request, 'shop/checkout.html', context)
        else:
            messages.error(request, 'Add product to Cart')
            return redirect('/')
    else:
        messages.error(request, 'Login required to Checkout')
        return redirect('/auth/login/')


# ============ END SECTION ====================
# ======================== SAVE ADDRESS AND PAYMENT=================
def orderPay(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            coupon = False
            addressId = request.POST.get('radio')
            code = request.POST.get('couponCode')
            address = Address.objects.get(id=addressId)
            user = request.user
            order = Order.objects.create(user=user, address=address, status="1")
            order.save()
            cart = Cart.objects.get(user=request.user)
            cartItem = CartItem.objects.filter(cart=cart)
            amt = 0
            for its in cartItem:
                amt += its.amt
                print(amt)
                ord_Prod = OrderProduct(order=order, qty=its.quantity, product=its.product, amt=its.amt, status="1")
                ord_Prod.save()
            subTotal = amt
            if code:
                coupon = Coupon.objects.get(code=code)
                coupUsed = CouponUsed(user=user, order=order, coupon=coupon)
                coupUsed.save()
                if amt >= coupon.condition:
                    amt -= coupon.discount
            order.amt = amt
            order.save()
            orderItem = OrderProduct.objects.filter(order=order)
            amt = amt * 100
            client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
            payment = client.order.create({'amount': amt, 'currency': 'INR', 'payment_capture': '1'})
            pay = Payment(order=order, razorpay_order_id=payment['id'], payment_id="")
            pay.save()
            context = {
                'order': order,
                'orderItems': orderItem,
                'paymentId': payment['id'],
                'key_id': settings.KEY_ID,
                'address': address,
                'coupon': coupon,
                'subTot': subTotal
            }
            return render(request, 'shop/razorpay.html', context)
    else:
        messages.error(request, 'Login to place order')
        return redirect('/auth/login/')


# ============ END SECTION ====================
# ==========RAZORPAY REDIRECT SUCCESS===========
@csrf_exempt
def handleRequest(request):
    response = request.POST
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }
    try:
        client.utility.verify_payment_signature(params_dict)
        pay = Payment.objects.get(razorpay_order_id=response['razorpay_order_id'])
        pay.successful = True
        pay.save()
        order = Order.objects.get(id=pay.order.id)
        order.active = True
        order.paid = True
        order.save()
        pay.payment_id = response['razorpay_payment_id']
        pay.save()
        cart = Cart.objects.get(user=request.user)
        cart.delete()
        messages.success(request, 'Payment Completed')
        return redirect('/')
    except:
        return redirect('/checkout/')


# ============ END SECTION ====================
# ============= CANCEL ORDERS ==================
@login_required
def cancelOrder(request, oid):
    order = Order.objects.get(id=oid, paid=True)
    payment = Payment.objects.get(order=order)
    client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
    amt = int(order.amt * 100)
    c = client.payment.refund(payment.payment_id, amt)
    refund_id = c['id']
    refund_status = c['status']
    refund = Refund(order=order, payment=payment, refund_id=refund_id, status=refund_status)
    refund.save()
    order.paid = False
    order.status="404"
    order.save()
    payment.refund=True
    payment.save()
    messages.success(request, 'Refund processed')
    return redirect('/')
