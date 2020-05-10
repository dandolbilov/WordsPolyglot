# -*- coding: utf-8 -*- 
"""
    File:    urls.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

import wdpt.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", wdpt.views.index, name="index"),
    path("ajax_get/", wdpt.views.ajax_get, name="ajax_get"),
    path("admin/", admin.site.urls),
]
