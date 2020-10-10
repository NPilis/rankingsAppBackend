from django.urls import include, path
from rest_framework import routers
from user.views import CurrentUser, UsersList, UserCreate, UserDetail
from ranking.views import UserRankings

app_name = 'users'

urlpatterns = [
    # path('', CurrentUser.as_view(), name='current-user'),
    path('', UsersList.as_view(), name='users-list'),
    path('create/', UserCreate.as_view(), name='user-create'),
    path('currentuser/', CurrentUser.as_view(), name='current-user'),
    path('<username>/', UserDetail.as_view(), name='user-detail'),
    path('<uuid:uuid>/rankings/', UserRankings.as_view(), name='user-rankings')
    # path('<uuid:uuid>/follow', follow_user, name='user-follow')
]