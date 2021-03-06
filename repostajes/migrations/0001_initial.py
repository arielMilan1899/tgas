# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-03-02 20:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0002_matricula'),
        ('fmaestros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repostaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
                ('albaran', models.CharField(max_length=16)),
                ('combustible', models.CharField(max_length=16)),
                ('litros', models.DecimalField(decimal_places=3, max_digits=10)),
                ('precio', models.DecimalField(decimal_places=3, max_digits=4)),
                ('importe', models.DecimalField(decimal_places=3, max_digits=10)),
                ('estacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fmaestros.Estacion')),
                ('matricula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Matricula')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
        ),
    ]
