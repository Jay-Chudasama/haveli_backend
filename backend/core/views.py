import datetime
import json
from random import randint

import razorpay as razorpay
import requests
from django.shortcuts import render, get_object_or_404
from paytmchecksum import PaytmChecksum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.settings import RZ_ID, RZ_KEY
from core.models import User, Otp, Token, Menu, CartItem, Item, Area, Order, OrderItemQuantity
from core.serializers import UserSerializer, MenuSerializer, OrderSerializer, OrderDetailSerializer, \
    NotificationSerializer
from core.utils import token_response, IsAuthenticatedUser, client, pagination


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
    fcmtoken = request.data.get('fcmtoken')

    if not otp or not phone:
        return Response("PARAMS_MISSING", status=400)

    try:
        obj = Otp.objects.get(phone=phone,otp=otp)
        obj.delete()

        user, created = User.objects.get_or_create(
            phone=phone,
        )
        user.fcmtoken = str(fcmtoken)
        user.save()

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
    area = request.GET.get('area')

    if not Area.objects.filter(name__iexact=area).exists():
        return Response("COMMING SOON...",status=400)



    menu = Menu.objects.filter(area__name__iexact=area,closed=False).first()
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

    CartItem.objects.get_or_create(user=request.user, item=item)
    return Response("SUCCESS")


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def remove_from_cart(request):
    id = request.data.get("id")

    CartItem.objects.filter(user=request.user, item__id=id).delete()

    return Response("SUCCESS")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def mycart(request):
    area = request.GET.get("area")

    delivery_charge =  get_object_or_404(Area,name__iexact=area).delivery_charge


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

    return Response({"delivery_charge":delivery_charge,"cart":data})


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def updateqty(request):
    id = request.GET.get('id')
    qty = request.GET.get('qty')
    cart_item = get_object_or_404(CartItem,user=request.user,item__id=id)
    cart_item.quantity=qty
    cart_item.save()

    return Response('SUCCESS')


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def initiate_payment(request):
    total_amount = request.data.get('total_amount')
    area = request.data.get('area')
    address = request.data.get('address')

    if not total_amount or not area or not address:
        return Response("PARAMS MISSING",status=400)

    request.user.address = address
    request.user.save()

    cartItems = CartItem.objects.filter(user=request.user,item__menu__closed=False)

    type = cartItems.first().item.menu.type

    item_price = 0
    for cartItem in cartItems:
        item_price = item_price + (cartItem.item.price*cartItem.quantity)

    delivery_charge = Area.objects.get(name__iexact=area).delivery_charge
    server_total_amount = item_price + delivery_charge

    if server_total_amount != total_amount:
        return Response("amount mismatched",status=400)


    print("initiating payment.... Please wait")
    res = client.order.create({
        "amount": server_total_amount*100,
        "currency": "INR",
        "receipt": str(request.user.id),
        "notes": {
            "area": area,
            "address": address,
        }
    })
    print(res)

    if not res.get('error'):
        order = Order()
        order.payment_status = res['status']
        order.id = res['id']
        order.type = type
        order.user = request.user
        order.address = address
        order.items_price = item_price
        order.delivery_price = delivery_charge
        order.total_amount = server_total_amount
        order.save()

        for cartItem in cartItems:
            OrderItemQuantity.objects.create(order=order, quantity=cartItem.quantity, item=cartItem.item)


        data = {
            "orderId": res['id'],
            "key": RZ_ID,
        }
        return Response(data)
    else:
        return Response({"detail": 'pg_request_failed'}, 400)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def verifypayment(request):

    order_id = request.data.get("id")
    py_id = request.data.get("py_id")
    signature = request.data.get("signature")

    verified = client.utility.verify_payment_signature({
        'razorpay_order_id': order_id,
        'razorpay_payment_id': py_id,
        'razorpay_signature': signature
    })

    if verified:
        CartItem.objects.filter(user=request.user).delete()

        order = get_object_or_404(Order,id=order_id)
        order.payment_status = 'paid'
        order.payment_id = py_id
        order.signature = signature
        order.save()
        return Response()
    else:
        order = get_object_or_404(Order,id=order_id)
        order.delete()
        return Response("tampered_request",status=403)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def paymentfailed(request):
    orderId = request.data.get('id')
    get_object_or_404(Order,id=orderId).delete()
    return Response("ORDER DELETED")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def orders(request):

    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    queryset = pagination.paginate_queryset(orders,request)

    data = OrderSerializer(queryset, many=True).data
    return pagination.get_paginated_response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def orderdetails(request):
    id = request.GET.get('id')

    order = get_object_or_404(Order,id=id)
    return Response(OrderDetailSerializer(order).data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def rating(request):
    id = request.GET.get('id')
    rating = request.GET.get('rating')

    order = get_object_or_404(Order,id=id)
    order.rating = rating
    order.save()

    return Response("SUCCESS")


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def name(request):
    name = request.data.get("name")
    request.user.name = name
    request.user.save()

    return Response("SUCCESS")



@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def notifications(request):

    request.user.notifications_set.filter(seen=False).update(seen=True)
    notifications_set = request.user.notifications_set.all().order_by('-created_at')

    queryset = pagination.paginate_queryset(notifications_set, request)

    data = NotificationSerializer(queryset, many=True).data
    return pagination.get_paginated_response(data)



