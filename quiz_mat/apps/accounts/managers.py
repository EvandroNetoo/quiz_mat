from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(
        self, email: str, password: str | None = None, **extra_fields
    ):
        if not email:
            raise ValueError('O campo email deve ser preenchido')

        email = self.normalize_email(email)
        user = self.model(
            email=email, **extra_fields
        )  # Usa self.model ao invés de User diretamente
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: str | None = None, **extra_fields
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Super usuários precisam ter 'is_staff=True'")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Super usuários precisam ter 'is_superuser=True'")

        return self.create_user(email, password, **extra_fields)
