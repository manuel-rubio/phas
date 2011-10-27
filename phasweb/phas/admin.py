from phas.models import Phas, Databases
from django.contrib import admin

class PhasAdmin(admin.ModelAdmin):
    list_display = ( 'module', 'version', 'created_at' )

class DatabasesAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'DSN', 'USR', 'PWD' )

admin.site.register(Phas, PhasAdmin)
admin.site.register(Databases, DatabasesAdmin)
