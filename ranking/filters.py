from ranking.models import Ranking, RankingPosition, Like, DisLike
from django.http import Http404

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

def get_ranking_position(query, position):
    try:
        return query.get(position=position)
    except RankingPosition.DoesNotExist:
        raise Http404("Ranking position does not exist.")