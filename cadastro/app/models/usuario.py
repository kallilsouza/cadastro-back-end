from django.db import models
from .endereco import Endereco
from django.contrib.auth.models import User, AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ValidationError
from validate_docbr import CPF, PIS

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT, null=True)
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True)
    pis = models.CharField(max_length=11, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome']

    class Meta:
        verbose_name = 'usuário'

    def __str__(self):
        return self.email

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        cpf_validator = CPF()
        pis_validator = PIS()
        if self.cpf:
            if not cpf_validator.validate(self.cpf):
                raise ValidationError('CPF inválido')
        if self.pis:
            if not pis_validator.validate(self.pis):
                raise ValidationError('PIS inválido')
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)