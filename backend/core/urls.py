from django.urls import path

from core.views import create_account

urlpatterns = [
    path('createaccount/', create_account),

]
