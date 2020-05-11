# -*- coding: utf-8 -*- 
"""
    File:    views.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import RankedWord, UserWord


def fmt_date(dt):
    # TODO: fix locale
    if 1:
        return dt.strftime("%Y-%m-%d %H:%M:%S %Z")
    else:
        from django.utils import dateformat
        return dateformat.format(dt, "Y-m-d H:i:s e")


def add_test_data():
    if not RankedWord.objects.count():
        RankedWord(listname='engCambridge', word='name', p_o_s='noun', level='A1').save()
        RankedWord(listname='engCambridge', word='name', p_o_s='verb', level='B1').save()
        RankedWord(listname='engCambridge', word='street', p_o_s='noun', level='A1').save()
        RankedWord(listname='engFreq5000', word='name', p_o_s='noun', rank=299).save()
        RankedWord(listname='engFreq5000', word='name', p_o_s='verb', rank=816).save()
        RankedWord(listname='engFreq5000', word='street', p_o_s='noun', rank=555).save()
    if not UserWord.objects.count():
        UserWord(listname='engDanA1', word='name', p_o_s='noun', urank=1, phrase1="What's the name of this street?").save()
        UserWord(listname='engDanA1', word='street', p_o_s='noun', urank=2, phrase1="Let's cross the street.").save()


def index(request):
    table_counters = {'RankedWord':RankedWord.objects.count(), 'UserWord':UserWord.objects.count()}
    return render(request, "index.html", {"table_counters": table_counters})


def ajax_get(request):
    resp_data = []

    tb = request.GET.get('tb', '')
    ln = request.GET.get('ln', '')
    if tb == 'ranked':
        for o in RankedWord.objects.filter(listname=ln):
            known = UserWord.objects.filter(word=o.word, p_o_s=o.p_o_s).count()
            d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'level', 'rank']}
            d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
            d.update({'known':'true' if known else 'false'})
            resp_data.append(d)
    elif tb == 'userwords':
        for o in UserWord.objects.filter(listname=ln):
            d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'urank', 'phrase1']}
            d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
            resp_data.append(d)

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put(request):
    resp_data = {'msg': ''}
    try:
        if request.method == "POST":
            obj = UserWord.objects.filter(id=request.POST['id']).first()
            if not obj:
                raise Exception('id not found')
            if obj.word != request.POST['word']:
                raise Exception('word mismatch')

            updated = []
            for field in ['phrase1']:
                new_val = request.POST[field]
                if new_val != getattr(obj, field):
                    setattr(obj, field, new_val)
                    updated.append(field)
            if updated:
                obj.save()
            resp_data['msg'] = 'updated: %s' % updated

    except Exception as ex:
        resp_data['msg'] = 'Exception: %s' % ex

    return HttpResponse(json.dumps(resp_data), content_type="application/json")
