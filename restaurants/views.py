# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from json import dumps

from django.db.models import QuerySet
from django.forms import model_to_dict
from django.views.generic import TemplateView

from restaurants.models import Restaurant


def extended_serializer(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, QuerySet):
        return list(obj)
    raise TypeError("{} could not be serialized".format(obj))


def calculate_weighted_grade(restaurant):
    # A lower weighted grade indicates a more sanitary restaurant. The value is based on the most recent grade and
    # inspection date.
    grade = restaurant["grades"][0]["score"] or 0
    violations = restaurant["inspections"][0]["score"] or 0
    # A restaurants grade is more important than the number of violations.
    return grade * 1000 + violations


class Home(TemplateView):
    template_name = "restaurants/home.html"

    def get_context_data(self, **kwargs):
        context_data = super(Home, self).get_context_data(**kwargs)
        top_restaurants = Restaurant.objects.filter(
            cuisine="Thai",
            grade__score__lte=2
        ).distinct()
        restaurant_list = []
        for restaurant in top_restaurants:
            restaurant_data = model_to_dict(restaurant)
            restaurant_data["borough"] = restaurant.get_borough_display()
            restaurant_data["grades"] = restaurant.grade_set.order_by("-date").values()
            restaurant_data["inspections"] = restaurant.inspection_set.order_by("-date").values()
            restaurant_list.append(restaurant_data)
        restaurant_list.sort(key=calculate_weighted_grade)
        context_data["restaurant_data"] = dumps(restaurant_list, default=extended_serializer)
        return context_data
