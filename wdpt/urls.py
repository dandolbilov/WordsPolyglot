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
    path("ajax/get/ranked/", wdpt.views.ajax_get_ranked),
    path("ajax/get/userwords/", wdpt.views.ajax_get_userwords),
    path("ajax/put/ranked/clicked/", wdpt.views.ajax_put_ranked_clicked),
    path("ajax/put/userwords/edited/", wdpt.views.ajax_put_userwords_edited),
    path("admin/", admin.site.urls),
]
