from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import  ModelSerializer

from core.models import User, Menu, Item, CartItem, Order, Notification


class UserSerializer(ModelSerializer):

    cart = SerializerMethodField()
    orders = SerializerMethodField()
    notifications = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','phone','name','cart','address',"orders","notifications"]

    def get_notifications(self, obj):
        list = obj.notifications_set.filter(seen=False)
        return len(list)
    def get_orders(self,user):
        return Order.objects.filter(user=user).count()

    def get_cart(self,user):
        items = CartItem.objects.filter(user=user,item__menu__closed=False)
        data = []
        for item  in items:
            data.append(item.item.id)

        return data


class MenuSerializer(ModelSerializer):

    items = SerializerMethodField()
    extras = SerializerMethodField()
    class Meta:
        model = Menu
        fields = ['id','banner','type','closing','items','extras']


    def get_items(self,menu):
        items = Item.objects.filter(menu=menu,extras=False)
        return ItemSerializer(items,many=True).data

    def get_extras(self, menu):
        items = Item.objects.filter(menu=menu, extras=True)
        return ItemSerializer(items, many=True).data


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields  = [ 'id','image','name','price']



class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','created_at','type','order_status']


class OrderDetailSerializer(ModelSerializer):
    items = SerializerMethodField()
    class Meta:
        model = Order
        fields = ['id','created_at','type','order_status','payment_id','payment_status','address','items_price','delivery_price','total_amount','items','rating']

    def get_items(self,order):
        orderItems = order.orderItems.all()
        data = []
        for orderItem in orderItems:
            json = ItemSerializer(orderItem.item).data
            json['quantity'] = orderItem.quantity
            data.append(json)

        return data


class NotificationSerializer(ModelSerializer):
    created_at = SerializerMethodField()
    class Meta:
        model = Notification
        fields = ['id','title','body','image','seen','created_at']


    def get_created_at(self, obj):
        return obj.created_at.strftime("%d %b %Y %H:%M %p")