# Generated by Django 2.1.1 on 2021-08-17 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('testcases', '0001_initial'),
        ('services', '0001_initial'),
        ('environments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(max_length=200)),
                ('startDate', models.DateTimeField()),
                ('lastRunId', models.CharField(blank=True, max_length=100, null=True)),
                ('nextRunTime', models.DateTimeField(blank=True, null=True)),
                ('crontab_schedule', models.IntegerField()),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='environments.Environment')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.Service')),
                ('tests', models.ManyToManyField(to='testcases.TestCase')),
            ],
            options={
                'db_table': 'schedules',
            },
        ),
    ]
