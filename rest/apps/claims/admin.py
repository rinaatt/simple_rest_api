from django.contrib import admin
from . import models as m


@admin.register(m.Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass
