# -*- coding: utf-8 -*- 
"""
    File:    views.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.shortcuts import render
from django.http import HttpResponse
from .models import BasicWord


def index(request):
    # add some test records if database is empty
    if not BasicWord.objects.count():
        BasicWord(lang='eng', word='name', p_o_s='noun|verb', level='A1', rank=299).save()
        BasicWord(lang='eng', word='street', p_o_s='noun', level='A1', rank=555).save()

    return render(request, "index.html", {"basic_words": BasicWord.objects.all()})
