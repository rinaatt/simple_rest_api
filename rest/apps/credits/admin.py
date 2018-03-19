from django.contrib import admin
from apps.credits import models as m


@admin.register(m.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', )


@admin.register(m.Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('created', 'name', 'organization', 'typ')
    list_display_links = ('name', )
    search_fields = ('name', 'organization__name', )
    date_hierarchy = 'created'
    list_filter = ('typ', )


@admin.register(m.Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created', 'partner', 'status', )
    search_fields = ('offer__name', 'partner__name', )
    date_hierarchy = 'created'
