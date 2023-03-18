from django.urls import path

from core.views import getotp, verifyotp, userdetails, logout, menu, add_to_cart, remove_from_cart, mycart, updateqty, \
    initiate_payment, verifypayment, paymentfailed, orders, orderdetails, rating, name, notifications

urlpatterns = [
    path('getotp/', getotp),
    path('verifyotp/', verifyotp),
    path('userdetails/', userdetails),
    path('menu/', menu),
    path('add/', add_to_cart),
    path('remove/', remove_from_cart),
    path('mycart/', mycart),
    path('updateqty/', updateqty),
    path('logout/', logout),
    path('initiatepayment/', initiate_payment),
    path('verifypayment/', verifypayment),
    path('paymentfailed/', paymentfailed),
    path('orders/', orders),
    path('orderdetails/', orderdetails),
    path('rating/', rating),
    path('name/', name),
    path('notifications/', notifications),
]