from django.db import models
import datetime

class Phas(models.Model):
    module = models.CharField(max_length=50)
    code = models.TextField()
    version = models.IntegerField(default=0)
    # FIXME: datetime.now deberia de ser usado ya que datetime.now() se cambia por la fecha
    # en el momento de la creacion.
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)

