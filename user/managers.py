from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password, **kwargs):
        if not email or not username:
            raise ValueError('Emai and username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **kwargs)
        user.set_password(password)
        if kwargs.get('is_superuser'):
            user.is_staff = True
        user.save()
        return user

    def create_superuser(self, email, username, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        superuser = self.create_user(
            email,
            username,
            password,
            **kwargs
        )

        return superuser
