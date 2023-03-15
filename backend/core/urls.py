from django.urls import path

from core.views import getotp, verifyotp, userdetails, logout, menu, add_to_cart, remove_from_cart, mycart

urlpatterns = [
    path('getotp/', getotp),
    path('verifyotp/', verifyotp),
    path('userdetails/', userdetails),
    path('menu/', menu),
    path('add/', add_to_cart),
    path('remove/', remove_from_cart),
    path('mycart/', mycart),
    path('logout/', logout),

]