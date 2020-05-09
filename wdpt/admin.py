# -*- coding: utf-8 -*- 
"""
    File:    admin.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.contrib import admin
from .models import BasicWord

admin.site.register(BasicWord)
