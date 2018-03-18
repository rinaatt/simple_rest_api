from django.contrib import admin
from apps.credits import models as m


@admin.register(m.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(m.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', )
    list_display_links = ('name', )


@admin.register(m.Claim)
class ClaimAdmin(admin.ModelAdmin):
    pass
