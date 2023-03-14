from django.urls import path

from core.views import getotp, verifyotp, userdetails, logout

urlpatterns = [
    path('getotp/', getotp),
    path('verifyotp/', verifyotp),
    path('userdetails/', userdetails),
    path('logout/', logout),
]