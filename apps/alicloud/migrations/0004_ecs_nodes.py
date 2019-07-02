# Generated by Django 2.1.7 on 2019-06-27 08:14

import alicloud.models.ecs
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0028_asset_type'),
        ('alicloud', '0003_auto_20190627_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecs',
            name='nodes',
            field=models.ManyToManyField(default=alicloud.models.ecs.default_node, related_name='ecs', to='assets.Node', verbose_name='Nodes'),
        ),
    ]
