# -*- coding: utf-8 -*- 
"""
    File:    views.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import RankedWord, UserWord


def fmt_date(dt):
    # TODO: fix locale
    if 1:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    else:
        from django.utils import dateformat
        return dateformat.format(dt, "Y-m-d H:i:s e")


def index(request):
    # add some test records if database is empty
    if not RankedWord.objects.count():
        RankedWord(listname='engCambridge', word='name', p_o_s='noun', level='A1').save()
        RankedWord(listname='engCambridge', word='name', p_o_s='verb', level='B1').save()
        RankedWord(listname='engCambridge', word='street', p_o_s='noun', level='A1').save()
        RankedWord(listname='engFreq5000', word='name', p_o_s='noun', rank=299).save()
        RankedWord(listname='engFreq5000', word='name', p_o_s='verb', rank=816).save()
        RankedWord(listname='engFreq5000', word='street', p_o_s='noun', rank=555).save()

    table_counters = {'RankedWord':RankedWord.objects.count(), 'UserWord':UserWord.objects.count()}
    return render(request, "index.html", {"table_counters": table_counters})


def ajax_get(request):
    resp_data = []
    for o in RankedWord.objects.all():
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'level', 'rank']}
        d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
        resp_data.append(d)
    return HttpResponse(json.dumps(resp_data), content_type="application/json")
