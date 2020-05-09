# -*- coding: utf-8 -*- 
"""
    File:    models.py
    Author:  Daniil Dolbilov
    Created: 13-Oct-2019
"""

from django.db import models


class BasicWord(models.Model):
    created = models.DateTimeField('Created', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True, auto_now_add=False)

    lang = models.CharField('Lang', max_length=20) # Language (eng, rus, deu, spa)
    word = models.CharField('Word', max_length=20)
    p_o_s = models.CharField('PoS', max_length=20, blank=True) # Part of speech (noun, verb, etc.)

    level = models.CharField('Level', max_length=20, blank=True) # CEF Level (A1, A2, B1, B2, C1, C2)
    rank = models.PositiveIntegerField('Rank', default=0) # Rank in frequency/personal list

    def __str__(self):
        return '%s (%s)' % (self.word, self.p_o_s)
