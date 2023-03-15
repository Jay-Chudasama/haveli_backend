from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import  ModelSerializer

from core.models import User, Menu, Item, CartItem


class UserSerializer(ModelSerializer):

    cart = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','phone','name','cart']

    def get_cart(self,user):
        items = CartItem.objects.filter(user=user,item__menu__closed=False)
        data = []
        for item  in items:
            data.append(item.id)

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



