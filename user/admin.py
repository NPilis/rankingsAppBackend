from django.contrib import admin
from .models import User

@admin.register(User)
class RankingAdmin(admin.ModelAdmin):
    list_display = ['email', 'uuid', 'username', 'date_joined', 'is_active']