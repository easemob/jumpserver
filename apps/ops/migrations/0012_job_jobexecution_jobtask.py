# Generated by Django 2.1.7 on 2020-07-17 02:44

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ops', '0011_auto_20200519_1841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Name')),
                ('description', models.CharField(max_length=128, verbose_name='Description')),
                ('crontab', models.CharField(blank=True, help_text='5 * * * *', max_length=128, null=True, verbose_name='Crontab')),
                ('is_periodic', models.BooleanField(default=False)),
                ('created_by', models.CharField(blank=True, default='', max_length=128)),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('start_job_task_id', models.CharField(default=None, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobExecution',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('executing', '正在执行'), ('finish', '完成'), ('cancel', '取消')], max_length=32)),
                ('execute_user', models.CharField(blank=True, default='system', max_length=128)),
                ('date_execute', models.DateTimeField(auto_now_add=True)),
                ('_task_execute_id', models.TextField()),
                ('_arguments_data', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ops.Job')),
            ],
        ),
        migrations.CreateModel(
            name='JobTask',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('job', models.CharField(max_length=64)),
                ('success_next_job_task_id', models.CharField(default=None, max_length=64)),
                ('failure_next_job_task_id', models.CharField(default=None, max_length=64)),
                ('task_meta', models.ManyToManyField(to='ops.TaskMeta')),
            ],
        ),
    ]
