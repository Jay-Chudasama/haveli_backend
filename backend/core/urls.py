from django.urls import path

from core.views import getotp, verifyotp, userdetails, updateprofile, news

urlpatterns = [
    path('getotp/', getotp),
    path('verifyotp/', verifyotp),
    path('userdetails/', userdetails),
    path('updateprofile/', updateprofile),
    path('news/', news),
]
