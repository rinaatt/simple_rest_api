from django.contrib import admin
from django.contrib.auth.models import User
from apps.common.constants import GROUP_PARTNERS
from . import models as m


class PartnerListFilter(admin.SimpleListFilter):
    title = 'Партнёр'
    parameter_name = 'partner'

    def lookups(self, request, model_admin):
        partner_users = User.objects\
            .filter(groups__name=GROUP_PARTNERS)\
            .values_list('pk', 'username')
        return tuple(partner_users)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(owner_id=self.value())
        return queryset


@admin.register(m.Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('created', 'surname', 'first_name', 'patronymic',
                    'phone_num', 'passport', 'owner')
    list_display_links = ('surname', 'first_name', 'patronymic', )
    list_filter = (PartnerListFilter, )

    def passport(self, obj):
        return '{} {}'.format(obj.pass_ser, obj.pass_num)
    passport.short_description = 'Номер паспорта'
