# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 03:11
from __future__ import unicode_literals

from django.db import migrations, models
import recipebook.models


class Migration(migrations.Migration):

    dependencies = [
        ('recipebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipebook',
            name='id',
            field=models.PositiveIntegerField(default=recipebook.models.create_unique_urlindex, primary_key=True, serialize=False),
        ),
    ]
