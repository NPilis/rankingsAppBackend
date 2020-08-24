from django.contrib import admin
from .models import Ranking, RankingPosition, Comment, Like, DisLike

@admin.register(Ranking)
class RankingAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'created_at', 'status', 'total_difference']
    list_filter = ['total_difference']

@admin.register(RankingPosition)
class RankingPositionAdmin(admin.ModelAdmin):
    list_display = ['title', 'ranking', 'position']

@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ['ranking', 'user', 'reply_to', 'created_at']

@admin.register(Like)
class Like(admin.ModelAdmin):
    list_display = ['user', 'ranking']

@admin.register(DisLike)
class DisLike(admin.ModelAdmin):
    list_display = ['user', 'ranking']