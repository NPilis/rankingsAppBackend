from ranking.models import Ranking, RankingPosition, Like, DisLike
from user.models import User
from django.http import Http404
from datetime import timedelta
from django.utils import timezone

def get_ranking(ranking_uuid):
    try:
        return Ranking.objects.get(uuid=ranking_uuid)
    except Ranking.DoesNotExist:
        raise Http404("Ranking does not exist.")

def get_like_if_exist(ranking, user):
    try:
        like = Like.objects.get(user=user, ranking=ranking)
    except Like.DoesNotExist:
        return False
    return like

def get_dislike_if_exist(ranking, user):
    try:
        dislike = DisLike.objects.get(user=user, ranking=ranking)
    except DisLike.DoesNotExist:
        return False
    return dislike

def get_ranking_position(query, id):
    try:
        return query.filter(id=id).first()
    except RankingPosition.DoesNotExist:
        raise Http404("Ranking position does not exist.")

def get_user(user_uuid):
    try:
        return User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        raise Http404("User does not exist.")

def set_time_range(days):
    curr_date = timezone.now()
    timestamp = curr_date - timedelta(days=days)
    return timestamp