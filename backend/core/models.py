from django.db import models


class User(models.Model):
    email = models.EmailField(max_length=500)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profiles/', null=True)
    bio = models.TextField(max_length=1000)


    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="follow_set")
    follow = models.ManyToManyField(User,blank=True,related_name="follow_user_set")


class Token(models.Model):
    token = models.CharField(max_length=5000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tokens_set")
    created_at = models.DateTimeField(auto_now_add=True)



class StoryImage(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="stories_set")
    image = models.ImageField(upload_to='profiles/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts_set")
    image = models.ImageField(upload_to='profiles/', null=True)
    caption = models.CharField(max_length=5000)
    likes = models.ManyToManyField(User,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications_set")
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    liked_by = models.ForeignKey(User,blank=True, on_delete=models.CASCADE, related_name="liked_notifications_set",null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)









