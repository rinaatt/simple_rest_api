from django.contrib import admin
from . import models as m


@admin.register(m.Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
