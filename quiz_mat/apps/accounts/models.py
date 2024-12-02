from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import validate_email
from django.db import models
from utils.models import Active, TimeStampedModel

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel, Active):
    class Meta:
        verbose_name = 'usuário'
        verbose_name_plural = 'usuários'

    email = models.EmailField(
        'email',
        unique=True,
        blank=False,
        validators=[validate_email],
    )

    name = models.CharField(
        'nome',
        max_length=150,
        blank=False,
    )

    is_staff = models.BooleanField(
        'status de staff',
        default=False,
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self) -> str:
        return self.email

    @property
    def first_name(self):
        return self.name.split(' ')[0]
