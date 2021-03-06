# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from contextlib import closing
from csv import DictReader
from datetime import datetime

import requests

from restaurants.models import Restaurant, Inspection, Grade

RESULT_SET_URL = "https://nycopendata.socrata.com/api/views/xx67-kt59/rows.csv?accessType=DOWNLOAD"


class TransformException(Exception):
    """
    Exception that get raised when data cannot be transformed to the expected format.
    """


def extract_restaurant_data(csv_obj):
    """
    Group restaurant data together.
    :param csv_obj: Object representing one row in a csv file.
    :return: Object.
    """
    return {
        "borough": csv_obj["BORO"],
        "building_number": csv_obj["BUILDING"],
        "cuisine": csv_obj["CUISINE DESCRIPTION"],
        "name": csv_obj["DBA"],
        "phone_number": csv_obj["PHONE"],
        "registration_number": csv_obj["CAMIS"],
        "street_name": csv_obj["STREET"],
        "zip_code": csv_obj["ZIPCODE"],
    }


def extract_inspection_data(csv_obj):
    """
    Group inspection data together.
    :param csv_obj: Object representing one row in a csv file.
    :return: Object.
    """
    return {
        "date": csv_obj["INSPECTION DATE"],
        "action": csv_obj["ACTION"],
        "violation_code": csv_obj["VIOLATION CODE"],
        "violation_description": csv_obj["VIOLATION DESCRIPTION"],
        "critical": csv_obj["CRITICAL FLAG"],
        "score": csv_obj["SCORE"],
        "check_type": csv_obj["INSPECTION TYPE"],
    }


def extract_grade_data(csv_obj):
    """
    Group grade data together.
    :param csv_obj: Object representing one row in a csv file.
    :return: Object.
    """
    return {
        "score": csv_obj["GRADE"],
        "date": csv_obj["GRADE DATE"],
    }


def transform_restaurant_data(extracted_data):
    """
    Transform restaurant data into the expected format.
    :param extracted_data: Object containing restaurant data extracted from a csv row.
    :return: None.
    """
    if extracted_data["cuisine"] != "Thai" or not extracted_data["name"]:
        # We only need to store Thai restaurants.
        raise TransformException("Restaurant does not serve Thai cuisine.")
    building_number = extracted_data.pop("building_number")
    street_name = extracted_data.pop("street_name")
    extracted_data["street_address"] = "{} {}".format(building_number, street_name)
    extracted_data["borough"] = extracted_data["borough"].lower()
    try:
        extracted_data["zip_code"] = int(extracted_data["zip_code"])
    except ValueError:
        raise TransformException("Restaurant data has an invalid zip code.")
    try:
        extracted_data["phone_number"] = int(extracted_data["phone_number"])
    except ValueError:
        extracted_data["phone_number"] = None
    extracted_data["registration_number"] = int(extracted_data["registration_number"])


def transform_inspection_data(extracted_data):
    """
    Transform inspection data into the expected format.
    :param extracted_data: Object containing inspection data extracted from a csv row.
    :return: None.
    """
    if not extracted_data["check_type"]:
        raise TransformException("Inspection data is missing: check type.")
    score = extracted_data["score"]
    extracted_data["critical"] = True if extracted_data["critical"] == "Critical" else False
    extracted_data["date"] = datetime.strptime(extracted_data["date"], "%m/%d/%Y")
    # Score is not a required field.
    extracted_data["score"] = int(score) if score else None


def transform_grade_data(extracted_data):
    """
    Transform grade data into the expected format.
    :param extracted_data: Object containing grade data extracted from a csv row.
    :return: None.
    """
    score = extracted_data["score"]
    date = extracted_data["date"]
    if not score or score == "Not Yet Graded":
        raise TransformException("Grade data is missing: score.")
    elif not date:
        raise TransformException("Grade data is missing: date")
    extracted_data["score"] = ord(score) - 64
    extracted_data["date"] = datetime.strptime(date, "%m/%d/%Y")


def load_restaurant_data(transformed_data):
    restaurant = Restaurant.objects.filter(registration_number=transformed_data["registration_number"]).first()
    if restaurant:
        for key, value in transformed_data.iteritems():
            setattr(restaurant, key, value)
        restaurant.save()
        return restaurant
    else:
        return Restaurant.objects.create(**transformed_data)


def load_inspection_data(restaurant, transformed_data):
    return Inspection.objects.create(restaurant=restaurant, **transformed_data)


def load_grade_data(restaurant, transformed_data):
    return Grade.objects.create(restaurant=restaurant, **transformed_data)


def run():
    line_number = 1
    # The data set is a big csv so we will have to stream it and process the rows one by one.
    with closing(requests.get(RESULT_SET_URL, stream=True)) as response:
        response.encoding = response.encoding or "utf-8"
        csv_obj_lines = DictReader(response.iter_lines())
        for csv_obj in csv_obj_lines:
            # Extract.
            restaurant_data = extract_restaurant_data(csv_obj)
            inspection_data = extract_inspection_data(csv_obj)
            grade_data = extract_grade_data(csv_obj)
            # Transform.
            valid_restaurant = valid_inspection = valid_grade = True
            try:
                transform_restaurant_data(restaurant_data)
            except TransformException:
                valid_restaurant = False
            try:
                transform_inspection_data(inspection_data)
            except TransformException:
                valid_inspection = False
            try:
                transform_grade_data(grade_data)
            except TransformException:
                valid_grade = False
            # Load.
            if valid_restaurant:
                restaurant = load_restaurant_data(restaurant_data)
                load_inspection_data(restaurant, inspection_data) if valid_inspection else None
                load_grade_data(restaurant, grade_data) if valid_grade else None
                print line_number, "Valid", restaurant.registration_number, restaurant.name
            else:
                print line_number, "Invalid", restaurant_data["registration_number"], restaurant_data["name"]
            # Setup.
            line_number += 1
