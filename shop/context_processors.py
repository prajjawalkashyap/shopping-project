from shop.models import Cart, CartItem, Category


def cartProcessor(request):
    if request.user.is_authenticated:
        categories=Category.objects.all()
        cart, created = Cart.objects.get_or_create(user=request.user)
        cartItems = CartItem.objects.filter(cart=cart)
        qty = 0
        total = 0.0
        for items in cartItems:
            qty += items.quantity
            total += items.amt

        return {'cartCount': qty, 'cartList': cartItems, 'cartTotal': total, 'category':categories}
    else:
        return {}