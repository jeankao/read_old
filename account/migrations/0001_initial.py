# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-06-17 10:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('event', models.CharField(max_length=100)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('title', models.CharField(max_length=250)),
                ('content', models.TextField(default=b'')),
                ('url', models.CharField(max_length=250)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MessageFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=0)),
                ('filename', models.TextField()),
                ('before_name', models.TextField()),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='MessagePoll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.IntegerField(default=0)),
                ('reader_id', models.IntegerField(default=0)),
                ('classroom_id', models.IntegerField(default=0)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PointHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('kind', models.IntegerField(default=0)),
                ('message', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=100)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('home_count', models.IntegerField(default=0)),
                ('visitor_count', models.IntegerField(default=0)),
                ('open_time', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=0)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VisitorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_id', models.IntegerField(default=0)),
                ('user_id', models.IntegerField(default=0)),
                ('IP', models.CharField(default=b'', max_length=20)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
