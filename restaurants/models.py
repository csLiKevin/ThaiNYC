# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Model, PositiveIntegerField, CharField, ForeignKey, IntegerField, SmallIntegerField, \
    PositiveSmallIntegerField, DateField, BooleanField


BOROUGHS = (
    ("bronx", "BRONX"),
    ("brooklyn","BROOKLYN"),
    ("manhattan", "MANHATTAN"),
    ("staten island", "STATEN ISLAND"),
    ("queens", "QUEENS"),
)

GRADES = (
    (1, "A"),
    (2, "B"),
    (3, "C"),
    (26, "Z")
)


class Restaurants(Model):
    borough = CharField(max_length=13, choices=BOROUGHS)
    cuisine = CharField(max_length=255)
    name = CharField(max_length=255)
    phone_number = PositiveIntegerField()
    registration_number = PositiveIntegerField(unique=True)
    street_address = CharField(max_length=255)
    zip_code = PositiveSmallIntegerField()


class Inspection(Model):
    action = CharField(max_length=255)
    check_type = CharField(max_length=255)
    critical = BooleanField(default=False)
    date = DateField()
    grade = IntegerField(choices=GRADES)
    grade_date = DateField()
    restaurant = ForeignKey(to=Restaurants)
    score = SmallIntegerField()
    violation_code = CharField(max_length=3)
    violation_description = CharField(max_length=255)

