# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-24 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0002_auto_20160920_0056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assetgroup',
            name='system_users',
            field=models.ManyToManyField(blank=True, related_name='asset_groups', to='assets.SystemUser'),
        ),
    ]