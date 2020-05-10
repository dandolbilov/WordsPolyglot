# -*- coding: utf-8 -*- 
"""
    File:    views.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import BasicWord


def fmt_date(dt):
    # TODO: fix locale
    if 1:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    else:
        from django.utils import dateformat
        return dateformat.format(dt, "Y-m-d H:i:s e")


def index(request):
    # add some test records if database is empty
    if not BasicWord.objects.count():
        BasicWord(lang='eng', word='name', p_o_s='noun|verb', level='A1', rank=299).save()
        BasicWord(lang='eng', word='street', p_o_s='noun', level='A1', rank=555).save()

    return render(request, "index.html", {"basic_words": BasicWord.objects.all()})


def ajax_get(request):
    resp_data = []
    for o in BasicWord.objects.all():
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'lang', 'word', 'p_o_s', 'level', 'rank']}
        d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
        resp_data.append(d)
    return HttpResponse(json.dumps(resp_data), content_type="application/json")
