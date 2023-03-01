from django.db import models

class User(models.Model):
    phone = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/',null=True)


class Otp(models.Model):
    phone = models.CharField(max_length=10)
    otp = models.IntegerField(default=0)


class News(models.Model):
    image = models.ImageField(upload_to='news/',)
    details = models.TextField(max_length=10000000)
    title = models.CharField(max_length=1000)


class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add=True)


