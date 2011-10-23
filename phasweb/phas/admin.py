from phas.models import Phas
from django.contrib import admin

class PhasAdmin(admin.ModelAdmin):
    list_display = ( 'module', 'version', 'created_at' )

admin.site.register(Phas, PhasAdmin)

