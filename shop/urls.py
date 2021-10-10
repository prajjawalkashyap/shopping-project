from django.urls import path
from shop.shopViews import jsonviews,headerviews,product,payment
from . import views
urlpatterns = [
    path('', views.shop, ),

    path('update_item/', jsonviews.updateItem, ),
    path('update/wishlist/',jsonviews.wishlist),
    path('moveToCart/',jsonviews.moveToCart),
    path('coupon/check/',jsonviews.couponCheck),

    path('myOrders/',headerviews.myOrder),
    path('wishlist/',headerviews.wishlistView),
    path('cart/', headerviews.cartView),

    path('product/<str:prod_id>/', product.prod_view),
    path('review/submit/',product.reviewSubmit),
    path('search/product/', product.searchProduct),

    path('checkout/', payment.checkout),
    path('order/pay/', payment.orderPay),
    path('cancel/order/<str:oid>/', payment.cancelOrder),
    path('success/', payment.handleRequest)
]
