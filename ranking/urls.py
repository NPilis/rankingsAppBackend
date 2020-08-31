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
    path('<uuid:uuid>/comment/', views.CommentRanking.as_view(), name='ranking-comment'),
    path('<uuid:uuid>/like/', views.RankingLike.as_view(), name='ranking-like'),
    path('<uuid:uuid>/dislike/', views.RankingDisLike.as_view(), name='ranking-dislike'),
    path('<uuid:uuid>/add-position/', views.add_position, name='ranking-add-position'), # Will be replaced by UpdateRanking
    path('<uuid:uuid>/delete/', views.DeleteRanking.as_view(), name='ranking-delete'),
    # path('<uuid:uuid>/update/, views.UpdateRanking.as_view(), name='ranking-update')
]
