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


def ajax_get_ranked(request):
    resp_data = []
    ln = request.GET.get('ln', '')
    for o in RankedWord.objects.filter(listname=ln):
        known = UserWord.objects.filter(word=o.word, p_o_s=o.p_o_s).count()
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'level', 'rank']}
        d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
        d.update({'known':'true' if known else 'false'})
        resp_data.append(d)
    return HttpResponse(json.dumps(resp_data), content_type="application/json")


def ajax_get_userwords(request):
    resp_data = []
    ln = request.GET.get('ln', '')
    for o in UserWord.objects.filter(listname=ln):
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'urank', 'phrase1']}
        d.update({'created':fmt_date(o.created), 'updated':fmt_date(o.updated)})
        resp_data.append(d)
    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_ranked_import(request):
    row_list = json.loads(request.body)
    ln = request.GET.get('ln', '')
    if row_list and row_list[0]['listname'] == ln:
        RankedWord.objects.filter(listname=ln).delete()  # CLEAR LIST
    for row in row_list:
        rw = RankedWord(listname=row['listname'], word=row['word'], p_o_s=row['p_o_s'], level=row['level'], rank=row['rank'])
        rw.save()
    resp_data = {'msg': 'imported: %s' % len(row_list)}
    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_ranked_clicked(request):
    resp_data = {'msg': ''}

    listname='engDanA1'  # TODO: listname
    p_word, p_pos = request.POST.get('word', ''), request.POST.get('p_o_s', '')

    if UserWord.objects.filter(listname=listname, word=p_word, p_o_s=p_pos).count():
        resp_data['msg'] = 'word exists'
    else:
        urank = UserWord.objects.filter(listname=listname).count() + 1
        uw = UserWord(listname=listname, word=p_word, p_o_s=p_pos, urank=urank)
        uw.save()
        resp_data['msg'] = 'word added'

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_userwords_clicked(request):
    p_list = request.POST.get('listname', '')
    p_word, p_pos = request.POST.get('word', ''), request.POST.get('p_o_s', '')

    del_num, del_dict = UserWord.objects.filter(listname=p_list, word=p_word, p_o_s=p_pos).delete()
    resp_data = {'msg': 'deleted: %s' % del_num}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_userwords_edited(request):
    resp_data = {'msg': ''}
    try:
        obj = UserWord.objects.filter(id=request.POST['id']).first()
        if not obj:
            raise Exception('id not found')
        if obj.word != request.POST['word']:
            raise Exception('word mismatch')

        updated = []
        for field in ['urank', 'phrase1']:
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
