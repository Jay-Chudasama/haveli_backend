from django.db import models

class User(models.Model):
    email = models.EmailField(max_length=500)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/',null=True)



class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add=True)


