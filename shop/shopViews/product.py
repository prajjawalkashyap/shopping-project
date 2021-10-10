from django.shortcuts import render, redirect
from shop.models import Product, Cart, CartItem, OrderProduct, Order, Payment, Review, Wishlist, ProductMedia, Coupon, \
    CouponUsed
from authy.models import User, Address
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# ===============SEARCH PRODUCT===========

def searchProduct(request):
    cat = request.POST.get('category')
    name = request.POST.get('search')
    if cat == 'all':
        product = Product.objects.filter(name__startswith=name)
    else:
        product = Product.objects.filter(name__startswith=name, category__name=cat)
    return render(request, 'shop/shop-grid.html', {'products': product})


# ============ END SECTION ====================
# ================PRODUCT VIEW=======================
def prod_view(request, prod_id):
    product = Product.objects.get(id=prod_id)
    review = Review.objects.filter(product=product)
    data = calculateReview(review)
    media = ProductMedia.objects.filter(product=product)
    context = {
        'product': product,
        'review': review,
        'rate': data['rate'], 'present': data['present'], 'avgStar': data['avg'],
        'starCount': data['star_list'], 'sum': data['total'], 'rate_list': data['rate_list'], 'count': data['c'],
        'media': media
    }
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartItem = CartItem.objects.filter(cart=cart, product=product)
        context['cartItems'] = cartItem
        wish = Wishlist.objects.filter(user=request.user, product=product)
        if wish:
            context['wishlist'] = wish[0]

    return render(request, 'shop/product.html', context)


# ============ END SECTION =============================
# ======================REVIEW SUBMITTING===============
@login_required
def reviewSubmit(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            rate = request.POST.get('rating')
            review = request.POST.get('review')
            pid = request.POST.get('pid')
            product = Product.objects.get(id=pid)
            rev = Review(user=request.user, product=product, rate=rate, comment=review)
            rev.save()
            return redirect('/product/' + str(pid))
    else:
        messages.error(request, 'Login to submit review')
        return redirect('/auth/login/')


# ============ END SECTION ====================
# ============================== CALCULATE RATING==================
def calculateReview(review):
    present = True
    total = 0
    avg = 0
    c = 0
    rate = [1, 2, 3, 4, 5]
    star_list = {}
    rate_list = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    try:
        for x in review:
            total = total + x.rate
            c += 1
            if x.rate in star_list.keys():
                star_list[x.rate] = star_list[x.rate] + 1
            else:
                star_list[x.rate] = 1
        for x in rate_list.keys():
            if x in star_list.keys():
                rate_list[x] = int((star_list[x] / c) * 100)
        avg = round((total / c), 1)
    except:
        present = False
    context = {
        'rate': rate,
        'present': present,
        'total': total,
        'avg': avg,
        'star_list': star_list,
        'c': c,
        'rate_list': rate_list
    }
    return context
# ============ END SECTION ====================
