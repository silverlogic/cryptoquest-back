# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-20 18:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faucets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='lat',
            field=models.DecimalField(blank=True, decimal_places=30, max_digits=40, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='lng',
            field=models.DecimalField(blank=True, decimal_places=30, max_digits=40, null=True),
        ),
    ]