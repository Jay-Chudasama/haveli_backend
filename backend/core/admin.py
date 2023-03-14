from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Otp, Token


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','phone','name']



@register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['id','phone','otp']





@register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ['id','token','user','created_at']