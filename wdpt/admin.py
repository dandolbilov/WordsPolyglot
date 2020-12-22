# -*- coding: utf-8 -*- 
"""
    File:    admin.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.contrib import admin
from .models.RankedWord import RankedWord
from .models.UserWord import UserWord


class RankedWordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RankedWord._meta.get_fields() if field.name not in ['id', 'created']]

class UserWordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserWord._meta.get_fields() if field.name not in ['id', 'created']]


admin.site.register(RankedWord, RankedWordAdmin)
admin.site.register(UserWord, UserWordAdmin)
