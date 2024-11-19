from django.db import models

class Operacion(models.Model):
    expresion = models.CharField(max_length=255)
    resultado = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)
