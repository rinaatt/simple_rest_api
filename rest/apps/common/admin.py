from django.contrib import admin
from . import models as m
# Register your models here.


@admin.register(m.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Offer)
class OfferAdmin(admin.ModelAdmin):
    pass
