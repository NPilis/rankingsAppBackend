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
