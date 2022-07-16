from django.db import models
from .endereco import Endereco
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from validate_docbr import CPF, PIS

class Usuario(models.Model):
    auth_user = models.OneToOneField(User, on_delete=models.CASCADE)
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT)
    cpf = models.CharField(max_length=11, unique=True)
    pis = models.CharField(max_length=11, unique=True)

    def nome(self):
        return f"{self.auth_user.first_name} {self.auth_user.last_name}"
    
    def email(self):
        return self.auth_user.email

    class Meta:
        verbose_name = 'usuário'

    def __str__(self):
        return self.auth_user.__str__()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        cpf_validator = CPF()
        pis_validator = PIS()
        if not cpf_validator.validate(self.cpf):
            raise ValidationError('CPF inválido')
        if not pis_validator.validate(self.pis):
            raise ValidationError('PIS inválido')
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)