from django.urls import include, path
from rest_framework import routers
from user.views import CurrentUser, UsersList, UserCreate, UserDetail

app_name = 'users'

urlpatterns = [
    # path('', CurrentUser.as_view(), name='current-user'),
    path('', UsersList.as_view(), name='users-list'),
    path('create/', UserCreate.as_view(), name='user-create'),
    path('<uuid:uuid>/', UserDetail.as_view(), name='user-detail'),
    path('currentuser/', CurrentUser.as_view(), name='current-user')
    # path('<uuid:uuid>/follow', follow_user, name='user-follow')
]