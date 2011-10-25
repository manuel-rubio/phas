from phas.models import Phas, BasesDeDatos
from django.contrib import admin

class PhasAdmin(admin.ModelAdmin):
    list_display = ( 'module', 'version', 'created_at' )

class BasesDeDatosAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'DSN', 'USR', 'PWD' )

admin.site.register(Phas, PhasAdmin)
admin.site.register(BasesDeDatos, BasesDeDatosAdmin)
