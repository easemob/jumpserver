# Generated by Django 2.1.7 on 2020-05-13 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0007_filedeployexecution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedeployexecution',
            name='dest',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='filedeployexecution',
            name='group',
            field=models.CharField(max_length=64, verbose_name='Group'),
        ),
        migrations.AlterField(
            model_name='filedeployexecution',
            name='mode',
            field=models.CharField(max_length=8, verbose_name='Mode'),
        ),
    ]
