# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2021-02-28 15:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apunte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('descripcion', models.CharField(max_length=60)),
                ('importe', models.DecimalField(decimal_places=2, max_digits=12)),
                ('es_gasto', models.BooleanField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Apunte Contable',
            },
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=16, unique=True)),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos de Gastos e Ingresos',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=16, unique=True)),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('razon_social', models.CharField(blank=True, max_length=60, null=True)),
                ('cif', models.CharField(blank=True, max_length=16, null=True)),
                ('cp', models.CharField(blank=True, max_length=11, null=True)),
                ('direccion', models.CharField(blank=True, max_length=70, null=True)),
                ('poblacion', models.CharField(blank=True, max_length=70, null=True)),
                ('provincia', models.CharField(blank=True, max_length=70, null=True)),
                ('telefono', models.CharField(blank=True, max_length=70, null=True)),
                ('pais', models.CharField(blank=True, max_length=70, null=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Empresas',
            },
        ),
        migrations.CreateModel(
            name='Estacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
                ('geo_latitud', models.DecimalField(decimal_places=16, max_digits=22)),
                ('geo_longitud', models.DecimalField(decimal_places=16, max_digits=22)),
                ('direccion', models.CharField(max_length=70)),
                ('petroleo_95', models.DecimalField(decimal_places=3, max_digits=4)),
                ('petroleo_diesel', models.DecimalField(decimal_places=3, max_digits=4)),
            ],
            options={
                'verbose_name_plural': 'Estaciones',
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=4, null=True, unique=True)),
                ('nombre', models.CharField(max_length=60, unique=True)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('fecha_paso_historico', models.DateTimeField(blank=True, default=None, null=True)),
            ],
            options={
                'verbose_name_plural': 'Provincias',
            },
        ),
        migrations.AddIndex(
            model_name='provincia',
            index=models.Index(fields=['codigo'], name='fmaestros_p_codigo_c61a39_idx'),
        ),
        migrations.AddField(
            model_name='estacion',
            name='provincia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fmaestros.Provincia'),
        ),
        migrations.AddField(
            model_name='apunte',
            name='cuenta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fmaestros.Cuenta'),
        ),
        migrations.AddIndex(
            model_name='estacion',
            index=models.Index(fields=['codigo'], name='fmaestros_e_codigo_1795ef_idx'),
        ),
        migrations.AddIndex(
            model_name='apunte',
            index=models.Index(fields=['fecha'], name='fmaestros_a_fecha_0ca71c_idx'),
        ),
        migrations.AddIndex(
            model_name='apunte',
            index=models.Index(fields=['es_gasto'], name='fmaestros_a_es_gast_a2d771_idx'),
        ),
        migrations.AddIndex(
            model_name='apunte',
            index=models.Index(fields=['cuenta'], name='fmaestros_a_cuenta__010029_idx'),
        ),
    ]