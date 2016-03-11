from django.db import models
from django.utils import timezone
from datetime import date

class Transaction(models.Model):
	tiempo_subida = models.DateTimeField(blank=True)
	user_id = models.IntegerField()
	x_subida = models.CharField(max_length=100)
	y_subida = models.CharField(max_length=100)
	tipo_transporte = models.CharField(max_length=100)
	serviciosentidovariante = models.CharField(max_length=100)
	tipo_dia = models.CharField(max_length=100)
	nviaje = models.IntegerField()
	netapa = models.IntegerField()
	x_bajada = models.CharField(max_length=100)
	y_bajada = models.CharField(max_length=100)
	tiempo_bajada = models.CharField(max_length=100)
	par_subida = models.CharField(max_length=100)
	par_bajada = models.CharField(max_length=100)
	zona_subida = models.CharField(max_length=100)
	zona_bajada = models.CharField(max_length=100)
	adulto = models.CharField(max_length=100)