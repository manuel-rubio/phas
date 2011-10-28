# -*- coding: utf-8 -*-
from phas.models import *
from django.contrib import admin

class PhasAdmin(admin.ModelAdmin):
    list_display = ( 'module', 'version' )

class DatabasesAdmin(admin.ModelAdmin):
	list_display = ( 'name', 'DSN' )

admin.site.register(Phas, PhasAdmin)
admin.site.register(Databases, DatabasesAdmin)
admin.site.register(Groups)
admin.site.register(TADAttrs)
admin.site.register(PhasAttrs)
admin.site.register(TAD)

