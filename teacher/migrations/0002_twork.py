# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-19 08:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TWork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('teacher_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
