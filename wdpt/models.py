# -*- coding: utf-8 -*- 
"""
    File:    models.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.db import models


class RankedWord(models.Model):
    created = models.DateTimeField('Created', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True, auto_now_add=False)

    listname = models.CharField('List Name', max_length=20) # Begins with Language (eng, rus, deu, spa), like 'engOxford'
    word = models.CharField('Word', max_length=20)
    p_o_s = models.CharField('PoS', max_length=20, blank=True) # Part of speech (noun, verb, etc.)

    level = models.CharField('Level', max_length=20, blank=True) # CEF Level (A1, A2, B1, B2, C1, C2)
    rank = models.PositiveIntegerField('Rank', default=0) # Rank in frequency/personal list

    def __str__(self):
        return '%s (%s)' % (self.word, self.p_o_s)

    def str_created(self):
        return self.created.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    def str_updated(self):
        return self.updated.strftime("%Y-%m-%d %H:%M:%S %Z") # TODO: fix locale

    @staticmethod
    def wlist_names():
        return [d['listname'] for d in RankedWord.objects.values('listname').distinct()]

    @staticmethod
    def import_rows(row_list, listname=''):
        imp_batch = []
        for o in row_list:
            ln = listname if listname else o.get('listname', '')
            rw = RankedWord(listname=ln, word=o.get('word', ''), p_o_s=o.get('p_o_s', ''),
                            level=o.get('level', ''), rank=o.get('rank', ''))
            imp_batch.append(rw)
        RankedWord.objects.bulk_create(imp_batch)

    @staticmethod
    def delete_by_listname(listname):
        del_num, _ = RankedWord.objects.filter(listname=listname).delete()
        return del_num


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
