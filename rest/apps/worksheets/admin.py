from django.contrib import admin
from . import models as m
# Register your models here.


@admin.register(m.Worksheet)
class WorksheetAdmin(admin.ModelAdmin):
    list_display = ('created', 'surname', 'first_name', 'patronymic',
                    'phone_num', 'passport')
    list_display_links = ('surname', 'first_name', 'patronymic', )

    def passport(self, obj):
        return '{} {}'.format(obj.pass_ser, obj.pass_num)
    passport.short_description = 'Номер паспорта'
