from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Token, StoryImage, Post, Notification, Follow, Book


class FollowInline(admin.TabularInline):
    model = Follow
    list_display = ['user','follow']

class NotificationInline(admin.TabularInline):
    model = Notification
    list_display = ['id','followed_by','liked_by','post','created_at']
    fk_name = "user"

class StoryImageInline(admin.TabularInline):
    model = StoryImage
    list_display = ['id', 'user', 'image','created_at' ]


class PostInline(admin.TabularInline):
    model = Post
    list_display = ['id', 'user', 'image','caption','likes','created_at' ]


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'username', 'image']
    inlines = [StoryImageInline,PostInline,NotificationInline,FollowInline]


@register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'token', 'user', 'created_at']





@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'author', 'pages']
