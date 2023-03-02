from django.urls import path

from core.views import create_account, login, forgot_password, setup_account, stories, homefeeds, add_post, search, \
    notifications, like, follow, userdetails, userfeeds, logout

urlpatterns = [
    path('createaccount/', create_account),
    path('login/', login),
    path('forgotpassword/', forgot_password),
    path('userdetails/', userdetails),
    path('setupaccount/', setup_account),
    path('stories/', stories),
    path('homefeeds/', homefeeds),
    path('addpost/', add_post),
    path('search/', search),
    path('notifications/', notifications),
    path('like/', like),
    path('follow/', follow),
    path('userfeeds/', userfeeds),
    path('logout/', logout),

]
