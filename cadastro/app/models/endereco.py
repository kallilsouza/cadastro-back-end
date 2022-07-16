from django.db import models

class Endereco(models.Model):
    pais = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'endereço'
        
    def __str__(self):
        return f"{self.rua}, {self.numero} ({self.cep}) - {self.municipio} ({self.estado}), {self.pais}"