# Generated by Django 2.1.1 on 2021-08-17 05:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestCase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='200 OK', max_length=120)),
                ('description', models.CharField(blank=True, max_length=120, null=True)),
                ('scheme', models.CharField(blank=True, max_length=120, null=True)),
                ('endpoint', models.CharField(max_length=120)),
                ('method', models.CharField(default='GET', max_length=120)),
                ('headers', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('params', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('requestBody', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('variables', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
            ],
            options={
                'db_table': 'testcases',
            },
        ),
    ]
