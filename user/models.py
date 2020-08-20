from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
import uuid

from .managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=40,
        unique=True,
        blank=False
    )
    username = models.CharField(
        max_length=40,
        blank=False,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,                
        unique=True,
        db_index=True
    )

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_followers(self):
        followers = Follow.objects.filter(user_to=self.user)
        return followers
    
    def get_following(self):
        followed_users = Follow.objects.filter(user_from=self.user)

class Follow(models.Model):
    user_from = models.ForeignKey(
        User,
        related_name="follow_creator",
        on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )
    followed = models.DateTimeField(auto_now_add=True,
                                    db_index=True)
    
    class Meta:
        ordering = ('-followed',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from,
                                      self.user_to)
