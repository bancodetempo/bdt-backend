from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must obviously have is_active=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(_('endereço de email'),
                              unique=True, blank=True, null=True)
    # id used to import users from the google drive spreadsheet
    google_drive_spreadsheet_id = models.CharField(max_length=256, unique=True)
    is_active = models.BooleanField(
        _('ativo'),
        default=True,
        help_text=_(
            'Indica se o usuário deve ser tratado como ativo. '
            'Desmarque esta opção ao invés de deletar o usuário.'
        ),
    )
    is_staff = models.BooleanField(
        _('administrador'),
        default=False,
        help_text=_('Indica se o usuário tem acesso à área administrativa.'),
    )
    date_joined = models.DateTimeField(
        _('data do cadastro'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    @classmethod
    def create_user(cls, email, password, is_active, is_staff):
        extra_fields = {}
        extra_fields['is_active'] = is_active
        extra_fields['is_staff'] = is_staff
        created_user = cls.objects.create_user(email, password, **extra_fields)
        return created_user
