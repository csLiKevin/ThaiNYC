# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 20:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inspection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('check_type', models.CharField(max_length=255)),
                ('critical', models.BooleanField(default=False)),
                ('date', models.DateField()),
                ('grade', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (26, 'Z')])),
                ('grade_date', models.DateField()),
                ('score', models.SmallIntegerField()),
                ('violation_code', models.CharField(max_length=3)),
                ('violation_description', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borough', models.CharField(choices=[('bronx', 'BRONX'), ('brooklyn', 'BROOKLYN'), ('manhattan', 'MANHATTAN'), ('staten island', 'STATEN ISLAND'), ('queens', 'QUEENS')], max_length=13)),
                ('cuisine', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('phone_number', models.PositiveIntegerField()),
                ('registration_number', models.PositiveIntegerField(unique=True)),
                ('street_address', models.CharField(max_length=255)),
                ('zip_code', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='inspection',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restaurants.Restaurants'),
        ),
    ]
