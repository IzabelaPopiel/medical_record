# Generated by Django 3.0.6 on 2020-06-02 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('pesel', models.CharField(max_length=11)),
                ('clinics', models.CharField(max_length=1000, blank=True, null=True)),
                ('chronic_conditions', models.CharField(max_length=1000, blank=True, null=True)),
            ],
        ),
    ]
