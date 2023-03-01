from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Token


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','username','image']





@register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','token','user','created_at']