from django.urls import path
from . import views
urlpatterns=[
    path('login/', views.loginPage, name="login page"),
    path('logout/', views.user_logout, name="logout page"),
    path('logging/', views.logging, name="logging in"),
    path('registration/', views.registration, name='registration'),
    path('activate/<uidb64>/<token>', views.activateView, name='activate'),
    path('address/submit/',views.addAddress,name="add address"),
    path('account/',views.account)
]