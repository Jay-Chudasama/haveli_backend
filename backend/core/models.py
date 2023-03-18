from django.db import models


class User(models.Model):
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=100,default="ENTER NAME")
    address = models.TextField(max_length=10000)
    fcmtoken = models.CharField(max_length=10000)


class Otp(models.Model):
    phone = models.CharField(max_length=10)
    otp = models.IntegerField(default=0)


class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add=True)


class Area(models.Model):
    name = models.CharField(max_length=1000)
    delivery_charge = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Menu(models.Model):
    choices = [
        ('LUNCH', 'LUNCH'),
        ('DINNER', 'DINNER'),
    ]
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    type = models.CharField(choices=choices, max_length=100)
    closing = models.DateTimeField()
    closed = models.BooleanField(default=False)

    banner = models.ImageField(upload_to="images")

    created_at = models.DateTimeField(auto_now_add=True)


class Item(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    extras = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Order(models.Model):
    id = models.CharField(primary_key=True,max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=5000)
    type = models.CharField(max_length=100)

    items_price = models.IntegerField(default=0)
    delivery_price = models.IntegerField(default=20)
    total_amount = models.IntegerField(default=0)

    statuses = [
        ("ACCEPTED", 'ACCEPTED'),
        ("PROCESSING", 'PROCESSING'),
        ("PACKED", 'PACKED'),
        ("OUT_FOR_DELIVERY", 'OUT_FOR_DELIVERY'),
        ("DELIVERED", 'DELIVERED'),
        ("FAILED", 'FAILED'),
    ]
    order_status = models.CharField(choices=statuses,default="ACCEPTED", max_length=100)
    rating = models.IntegerField(default=0)

    payment_statuses = [
        ("created", "created"),
        ("attempted", "attempted"),
        ("paid", "paid"),
    ]
    payment_status = models.CharField(choices=payment_statuses,max_length=100)
    payment_id = models.CharField(max_length=5000)
    signature = models.TextField(max_length=5000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItemQuantity(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name="orderItems")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications_set")
    title = models.CharField(max_length=225)
    body = models.TextField(max_length=1000)
    seen = models.BooleanField(default=False)
    image = models.ImageField(upload_to="notifications/",blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

