from django.contrib import admin
from django.contrib.admin import register

from core.models import User, Otp, News


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','phone','name','image']



@register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['id','phone','otp']


@register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['id','title','details','image']