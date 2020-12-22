# -*- coding: utf-8 -*- 
"""
    File:    Sentence.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.db import models


class Sentence(models.Model):
    created = models.DateTimeField('Created', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True, auto_now_add=False)

    listname = models.CharField('List Name', max_length=20)
    phrase = models.CharField('Phrase', max_length=100)
    phrase_id = models.CharField('PhraseID', max_length=20)

    def __str__(self):
        return '%s : %s' % (self.phrase_id, self.phrase)

    def str_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    def str_updated(self):
        return self.updated.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    @staticmethod
    def wlist_names():
        return [d['listname'] for d in Sentence.objects.values('listname').distinct()]

    @staticmethod
    def import_rows(row_list, listname=''):
        imp_batch = []
        for o in row_list:
            ln = listname if listname else o.get('listname', '')
            rw = Sentence(listname=ln, phrase=o.get('phrase', ''), phrase_id=o.get('phrase_id', ''))
            imp_batch.append(rw)
        Sentence.objects.bulk_create(imp_batch)

    @staticmethod
    def delete_by_listname(listname):
        del_num, _ = Sentence.objects.filter(listname=listname).delete()
        return del_num

    @staticmethod
    def find_by_word(word, limit):
        return Sentence.objects.filter(phrase__contains=' '+word+' ')[0: limit]

    @staticmethod
    def html_by_word(word, limit):
        tt = 'https://tatoeba.org/eng/sentences/show/'
        return '<br/>'.join([f'<a href="{tt}{w.phrase_id}">{w.phrase}</a>' for w in Sentence.find_by_word(word, limit)])
