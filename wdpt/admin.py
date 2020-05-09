# -*- coding: utf-8 -*- 
"""
    File:    admin.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.contrib import admin
from .models import BasicWord


class BasicWordAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BasicWord._meta.get_fields() if field.name not in ['id', 'created']]


admin.site.register(BasicWord, BasicWordAdmin)
