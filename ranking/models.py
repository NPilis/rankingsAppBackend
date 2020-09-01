import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import IntegrityError, models
from django.urls import reverse
from django.utils.text import slugify

UserModel = get_user_model()

class Ranking(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('public', 'Public')
    )
    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='rankings'
    )
    title = models.CharField(max_length=40)
    content = models.CharField(
        max_length=200,
        blank=True
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='private'
    )
    image = models.ImageField(blank=True)
    uuid = models.UUIDField(
        unique=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='likes',
        blank=True
    )
    dislikes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='dislikes',
        blank=True
    )
    comments = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='comments',
        blank=True,
        through='Comment'
    )
    shares = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='shares',
        blank=True,
        through='Share'
    )
    total_difference = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-total_difference',)

    def __str__(self):
        return self.title

class RankingPosition(models.Model):
    title = models.CharField(max_length=40)
    ranking = models.ForeignKey(
        Ranking,
        related_name='ranking_positions',
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=1)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            ranking_positions = self.ranking.ranking_positions.all()
            if ranking_positions:
                self.position = ranking_positions.last().position + 1
        super(RankingPosition, self).save(*args, **kwargs)

    class Meta:
        ordering = ('ranking', 'position')

class Comment(models.Model):

    ranking = models.ForeignKey(
        Ranking,
        on_delete=models.CASCADE,
        related_name="ranking_comments",
    )
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name="user_comments",
    )
    reply_to = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
        
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return '{} commented {}'.format(self.user, self.ranking)

    
class Like(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)

    def __str__(self):
        return '{} likes {}'.format(self.user.username, self.ranking.title)
    
    def save(self, *args, **kwargs):
        self.ranking.likes.add(self.user)
        super(Like, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.ranking.likes.remove(self.user)
        super(Like, self).delete(*args, **kwargs)

class DisLike(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)

    def __str__(self):
        return '{} dislikes {}'.format(self.user.username, self.ranking.title)

    def save(self, *args, **kwargs):
        self.ranking.dislikes.add(self.user)
        super(DisLike, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        self.ranking.dislikes.remove(self.user)
        super(DisLike, self).delete(*args, **kwargs)

        
class Share(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, on_delete=models.CASCADE)

    def __str__(self):
        return '{} shared {}'.format(self.user.username, self.ranking.title)
    