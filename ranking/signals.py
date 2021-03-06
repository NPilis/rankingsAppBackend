from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Ranking, RankingPosition

@receiver(m2m_changed, sender=Ranking.dislikes.through)
@receiver(m2m_changed, sender=Ranking.likes.through)
def ranking_like_changed(sender, instance, **kwargs):
    """
    Update ranking total difference when liking or disliking
    """
    instance.total_difference = instance.likes.count() - instance.dislikes.count()
    instance.save()
