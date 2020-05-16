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


def index(request):
    table_counters = {'RankedWord':RankedWord.objects.count(), 'UserWord':UserWord.objects.count()}
    return render(request, "index.html", {"table_counters": table_counters,
                "ranked_names": RankedWord.wlist_names(), "userwords_names": UserWord.wlist_names()
                })


def ajax_get_ranked(request):
    resp_data = []
    ln = request.GET.get('ln', '')

    page_size = int(request.GET.get('size', '10000'))
    page_num  = int(request.GET.get('page', '0'))
    offset = (page_num - 1) * page_size if page_num else 0

    extra_column = {'known': "select count(1) from wdpt_userword where wdpt_userword.word = wdpt_rankedword.word and wdpt_userword.p_o_s = wdpt_rankedword.p_o_s"}
    for o in RankedWord.objects.filter(listname=ln).extra(select=extra_column).order_by('known', 'rank', 'level')[offset: offset + page_size]:
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'level', 'rank']}
        d.update({'created': o.str_created(), 'updated': o.str_updated()})
        d.update({'known':'true' if o.known else 'false'})
        resp_data.append(d)

    if page_num:
        # change response format for "remote pagination"
        last_page = (RankedWord.objects.filter(listname=ln).count() + page_size - 1) // page_size
        resp_data = {"last_page":last_page, "data":resp_data}

    return HttpResponse(json.dumps(resp_data), content_type="application/json")


def ajax_get_userwords(request):
    resp_data = []
    ln = request.GET.get('ln', '')
    for o in UserWord.objects.filter(listname=ln):
        d = {k:v for k,v in o.__dict__.items() if k in ['id', 'listname', 'word', 'p_o_s', 'urank', 'phrase1']}
        d.update({'created': o.str_created(), 'updated': o.str_updated()})
        resp_data.append(d)
    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_ranked_import(request):
    rows = json.loads(request.body)
    ln = request.GET.get('ln', '')

    del_num = RankedWord.delete_by_listname(ln)  # CLEAR LIST
    RankedWord.import_rows(row_list=rows, listname=ln)

    resp_data = {'msg': f'deleted: {del_num}, imported: {len(rows)}'}
    return HttpResponse(json.dumps(resp_data), content_type="application/json")


@csrf_exempt
def ajax_put_userwords_import(request):
    rows = json.loads(request.body)
    ln = request.GET.get('ln', '')

    del_num = UserWord.delete_by_listname(ln)  # CLEAR LIST
    UserWord.import_rows(row_list=rows, listname=ln)

    resp_data = {'msg': f'deleted: {del_num}, imported: {len(rows)}'}
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
