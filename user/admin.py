from django.contrib import admin
from .models import User, Follow

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'uuid', 'username', 'date_joined', 'is_active']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'followed']