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
            name='Environment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('url', models.CharField(max_length=120)),
                ('variables', django.contrib.postgres.fields.jsonb.JSONField(default=list)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
            ],
            options={
                'db_table': 'environments',
                'ordering': ['id'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='environment',
            unique_together={('name', 'service')},
        ),
    ]