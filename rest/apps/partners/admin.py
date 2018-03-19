from django.contrib import admin
from . import models as m


@admin.register(m.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', )
    search_fields = ('name', )


class PartnerListFilter(admin.SimpleListFilter):
    title = 'Партнёр'
    parameter_name = 'partner'

    def lookups(self, request, model_admin):
        partners = m.Organization.objects.values_list('pk', 'name')
        return tuple(partners)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(organization_id=self.value())
        return queryset


@admin.register(m.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('created', 'surname', 'first_name', 'patronymic',
                    'phone_num', 'passport', 'organization')
    list_display_links = ('surname', 'first_name', 'patronymic', )
    list_filter = (PartnerListFilter, )
    search_fields = ('surname', 'first_name', 'pass_num', )
    date_hierarchy = 'created'

    def passport(self, obj):
        return '{} {}'.format(obj.pass_ser, obj.pass_num)
    passport.short_description = 'Номер паспорта'
