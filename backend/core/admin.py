from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Otp, Token, Menu, Item, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    list = ['id','item','quantity']

@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','phone','name']
    inlines = [CartItemInline]



@register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['id','phone','otp']





@register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','token','user','created_at']


class ItemInline(admin.TabularInline):
    model = Item
    list = ['id','name','image','price','extras','created_at']

@register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id','banner','type','closing','closed','created_at']
    inlines = [ItemInline]

    def has_add_permission(self, request):
        menu_exists = Menu.objects.filter(closed=False).exists()
        return not menu_exists

    def has_change_permission(self, request, obj=None):
        if obj:
            return not obj.closed

        return True

    def has_delete_permission(self, request, obj=None):
        return False

