from django.db import models

class User(models.Model):
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=100)


class Otp(models.Model):
    phone = models.CharField(max_length=10)
    otp = models.IntegerField(default=0)




class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add=True)


class Menu(models.Model):
    choices = [
        ('LUNCH','LUNCH'),
        ('DINNER','DINNER'),
    ]
    type = models.CharField(choices=choices,max_length=100)
    closing = models.DateTimeField()
    closed = models.BooleanField(default=False)

    banner = models.ImageField(upload_to="images")

    created_at  = models.DateTimeField(auto_now_add=True)



class Item(models.Model):
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    extras = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)





