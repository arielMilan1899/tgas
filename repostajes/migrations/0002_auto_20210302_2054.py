# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-03-02 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repostajes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repostaje',
            name='codigo',
        ),
        migrations.RemoveField(
            model_name='repostaje',
            name='fecha_paso_historico',
        ),
        migrations.RemoveField(
            model_name='repostaje',
            name='observaciones',
        ),
        migrations.AlterField(
            model_name='repostaje',
            name='albaran',
            field=models.CharField(max_length=16, unique=True),
        ),
    ]
