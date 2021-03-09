# Generated by Django 2.2.6 on 2020-05-16 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wdpt', '0002_auto_20200510_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('listname', models.CharField(max_length=20, verbose_name='List Name')),
                ('phrase', models.CharField(max_length=100, verbose_name='Phrase')),
                ('phrase_id', models.CharField(max_length=20, verbose_name='PhraseID')),
            ],
        ),
    ]