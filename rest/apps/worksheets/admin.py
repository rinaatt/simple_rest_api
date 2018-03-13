from django.contrib import admin
from . import models as m
# Register your models here.


@admin.register(m.Worksheet)
class WorksheetAdmin(admin.ModelAdmin):
    pass
