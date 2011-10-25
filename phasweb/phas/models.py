from django.db import models
import datetime

class Phas(models.Model):
    module = models.CharField(max_length=50)
    code = models.TextField()
    version = models.IntegerField(default=0)
    # FIXME: datetime.now deberia de ser usado ya que datetime.now() se cambia por la fecha
    # en el momento de la creacion.
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)

class BasesDeDatos(models.Model):
	name = models.CharField(max_length=50, unique=True)
	DSN = models.CharField(max_length=256)
	USR = models.CharField(max_length=50, null=True, blank=True)
	PWD = models.CharField(max_length=50, null=True, blank=True)
