# Generated by Django 2.1.1 on 2021-08-17 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('testcases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assertion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comparator', models.CharField(max_length=120)),
                ('property', models.CharField(blank=True, max_length=120, null=True)),
                ('source', models.CharField(max_length=120)),
                ('target', models.CharField(max_length=120)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testcases.TestCase')),
            ],
            options={
                'db_table': 'assertions',
            },
        ),
    ]
