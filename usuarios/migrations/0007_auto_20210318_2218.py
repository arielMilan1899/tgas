# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-03-18 22:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0006_auto_20210305_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fmaestros.Provincia'),
        ),
    ]
