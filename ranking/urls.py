# from .views import CurrentRanking, CreateRanking, RankingPublicList, RankingPrivateList, RankingDetail
from django.urls import path

from ranking.models import Ranking, RankingPosition

from . import views

app_name = 'rankings'

urlpatterns = [
    path('<int:pk>/', views.CurrentRanking.as_view(), name='current-user'),
    # path('<int:pk>/', views.RankingDetail.as_view(), name='ranking-detail'),
    path('<uuid:uuid>/', views.RankingDetail.as_view(), name='ranking-detail'),
    path('private/', views.RankingPrivateList.as_view(), name='users-list'),
    path('public/', views.RankingPublicList.as_view(), name='user-create'),
    path('create/', views.CreateRanking.as_view(), name="create-ranking"),
    path('<uuid:uuid>/comment/', views.CommentRanking.as_view(), name='ranking-comment'),
    path('<uuid:uuid>/<str:action>/', views.ranking_like, name='ranking-like')
]
