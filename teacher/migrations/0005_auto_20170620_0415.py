# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-19 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0004_auto_20170620_0331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fcontent',
            name='content_file',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='fcontent',
            name='content_link',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='fcontent',
            name='content_youtube',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
