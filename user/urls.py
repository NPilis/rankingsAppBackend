from django.urls import include, path
from rest_framework import routers
from user.views import CurrentUser, UsersList, UserCreate

app_name = 'user'

urlpatterns = [
    path('', CurrentUser.as_view(), name='current-user'),
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/create', UserCreate.as_view(), name='user-create')
]