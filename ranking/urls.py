# from .views import CurrentRanking, CreateRanking, PublicRankings, PrivateRankings, RankingDetail
from django.urls import path

from ranking.models import Ranking, RankingPosition

from . import views

app_name = 'rankings'

urlpatterns = [
    path('<uuid:uuid>/', views.RankingDetail.as_view(), name='ranking-detail'),
    path('private/', views.PrivateRankings.as_view(), name='users-list'),
    path('public/', views.PublicRankings.as_view(), name='user-create'),
    path('create/', views.CreateRanking.as_view(), name="create-ranking"),
    path('followed/', views.FollowedUsersRankings.as_view(), name="followed-users-rankings"),
    path('<uuid:uuid>/delete/', views.DeleteRanking.as_view(), name='ranking-delete'),
    path('<uuid:uuid>/edit/', views.EditRanking.as_view(), name='ranking-edit'),
    path('<uuid:uuid>/create-rp/', views.RankingPositionsCreate.as_view(), name='ranking-position-create'),
    path('<uuid:uuid>/delete-rp/<int:id>/', views.RankingPositionDelete.as_view(), name='ranking-position-delete'),
    path('<uuid:uuid>/update-rp/<int:id>/', views.RankingPositionUpdate.as_view(), name='ranking-position-update'),
    path('<uuid:uuid>/like/', views.RankingLike.as_view(), name='ranking-like'),
    path('<uuid:uuid>/dislike/', views.RankingDisLike.as_view(), name='ranking-dislike'),
    path('<uuid:uuid>/comments/', views.RankingComments.as_view(), name='ranking-comments'),
    path('<uuid:uuid>/edit/change-positions/', views.ChangePositions.as_view(), name='change-positions')
]
