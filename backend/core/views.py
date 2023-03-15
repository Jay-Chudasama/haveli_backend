import datetime
from random import randint

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from core.models import User, Otp, Token, Menu, CartItem, Item
from core.serializers import UserSerializer, MenuSerializer
from core.utils import token_response, IsAuthenticatedUser


@api_view(['POST'])
def getotp(request):
    phone = request.data.get('phone')

    if not phone:
        return Response("PARAMS_MISSING",status=400)

    # otp = randint(1000, 9999) todo
    otp = 1234
    print(otp)

    obj, created = Otp.objects.update_or_create(
        phone=phone,
        defaults={'phone': phone,'otp':otp},
    )
    return Response("SUCCESS")


@api_view(['POST'])
def verifyotp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    if not otp or not phone:
        return Response("PARAMS_MISSING", status=400)

    try:
        obj = Otp.objects.get(phone=phone,otp=otp)
        obj.delete()

        user, created = User.objects.get_or_create(
            phone=phone,

        )

        return token_response(user)
    except:
        return Response("Invalid otp",status=400)



@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userdetails(request):
    data = UserSerializer(request.user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def logout(request):
    Token.objects.filter(user=request.user).delete()
    return Response("LOGGED OUT")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def menu(request):
    menu = Menu.objects.filter(closed=False).first()
    if menu and datetime.datetime.now(menu.closing.tzinfo) > menu.closing:
        menu.closed = True
        menu.save()
        menu = None

    data = {
        "type" : None
    }
    if menu:
        data = MenuSerializer(menu).data

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def add_to_cart(request):
    id = request.data.get("id")
    item = get_object_or_404(Item,id=id)

    if item.menu.closed:
        return Response("Closed",status=400)

    CartItem.objects.create(user=request.user, item=id)
    return Response("SUCCESS")


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def remove_from_cart(request):
    id = request.data.get("id")

    CartItem.objects.filter(user=request.user, item=id).delete()

    return Response("SUCCESS")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def mycart(request):

    cart_items = CartItem.objects.filter(user=request.user,item__menu__closed=False)

    data = []
    for cart_item in cart_items:
        data.append({
            'id':cart_item.item.id,
            'image':cart_item.item.image.url,
            'name':cart_item.item.name,
            'quantity':cart_item.quantity,
            'price':cart_item.item.price,
        })

    return Response(data)

