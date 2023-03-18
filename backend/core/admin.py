from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Otp, Token, Menu, Item, CartItem, Area, Order, OrderItemQuantity, Notification
from core.utils import send_user_notification


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


@register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['name','delivery_charge']

    def has_delete_permission(self, request, obj=None):
        return False


@register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id','area','banner','type','closing','closed','created_at']
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



class OrderItemsQuantityInline(admin.TabularInline):
    model = OrderItemQuantity
    list = ['item','quantity']

def notify(order):
    user = order.user
    title = "ORDER " + order.order_status
    body = "Your " + order.type + " has been " + order.order_status + "."
    image = order.orderItems.first().item.image
    print(image)
    print("ORDER STATUS: " + title)
    send_user_notification(user, title, body, image)
@register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','user','items_price','delivery_price','rating','total_amount','order_status','payment_status','payment_id','signature','created_at','updated_at']
    inlines = [OrderItemsQuantityInline]

    list_filter = ['order_status','payment_status']

    def mark_as_processing(modeladmin, request, queryset):
        for order in queryset:
            order.order_status = 'PROCESSING'
            order.save()
            notify(order)
    mark_as_processing.short_description = 'Mark as PROCESSING'

    def mark_as_packed(modeladmin, request, queryset):
        for order in queryset:
            order.order_status = 'PACKED'
            order.save()
            notify(order)

    mark_as_packed.short_description = 'Mark as PACKED'

    def mark_as_out_for_delivery(modeladmin, request, queryset):
        for order in queryset:
            order.order_status = 'OUT_FOR_DELIVERY'
            order.save()
            notify(order)

    mark_as_out_for_delivery.short_description = 'Mark as OUT_FOR_DELIVERY'

    def mark_as_delivered(modeladmin, request, queryset):
        for order in queryset:
            order.order_status = 'DELIVERED'
            order.save()
            notify(order)

    mark_as_delivered.short_description = 'Mark as DELIVERED'



    actions = [mark_as_processing,mark_as_packed,mark_as_out_for_delivery,mark_as_delivered]

    def save_model(self, request, order, form, change):
        super(OrderAdmin, self).save_model(request, order, form, change)
        notify(order)



@register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'body', 'image', 'seen', 'created_at']