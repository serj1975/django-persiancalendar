# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateField(verbose_name='date published'),
        ),
    ]
