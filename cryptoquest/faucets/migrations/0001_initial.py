# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-20 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('coins', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faucet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coins', to='coins.Coin')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='faucet',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faucets', to='faucets.Location'),
        ),
    ]