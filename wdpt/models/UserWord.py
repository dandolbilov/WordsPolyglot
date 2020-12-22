# -*- coding: utf-8 -*- 
"""
    File:    UserWord.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.db import models


class UserWord(models.Model):
    created = models.DateTimeField('Created', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True, auto_now_add=False)

    listname = models.CharField('List Name', max_length=20)
    word = models.CharField('Word', max_length=20)
    p_o_s = models.CharField('PoS', max_length=20, blank=True)

    urank = models.PositiveIntegerField('URank', default=0) # Ranked by user (position in list)
    phrase1 = models.CharField('Phrase1', max_length=50, blank=True)
    examples = models.CharField('Examples', max_length=50, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.word, self.p_o_s)

    def str_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    def str_updated(self):
        return self.updated.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    @staticmethod
    def wlist_names():
        return [d['listname'] for d in UserWord.objects.values('listname').distinct()]

    @staticmethod
    def import_rows(row_list, listname=''):
        imp_batch = []
        for o in row_list:
            ln = listname if listname else o.get('listname', '')
            uw = UserWord(listname=ln, word=o.get('word', ''), p_o_s=o.get('p_o_s', ''),
                        urank=o.get('urank', ''), phrase1=o.get('phrase1', ''),
                        examples=o.get('examples', ''))
            imp_batch.append(uw)
        UserWord.objects.bulk_create(imp_batch)

    @staticmethod
    def delete_by_listname(listname):
        del_num, _ = UserWord.objects.filter(listname=listname).delete()
        return del_num
