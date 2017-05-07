# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.test import TestCase

from restaurants.etl import extract_restaurant_data, extract_inspection_data, extract_grade_data, \
    transform_restaurant_data, transform_inspection_data, transform_grade_data, TransformException


class ExtractTestCases(TestCase):
    def setUp(self):
        self.building_number = "152"
        self.borough = "BROOKLYN"
        self.critical = "Not Critical"
        self.restaurant_name = "LEE'S VILLA CHINESE RESTAURANT"
        self.inspection_date = "10/28/2015"
        self.cuisine = "Chinese"
        self.zip_code = "11201"
        self.violation_code = "10B"
        self.inspection_type = "Cycle Inspection / Re-inspection"
        self.phone = "7188551818"
        self.street_name = "LAWRENCE STREET"
        self.registration_number = "40388386"
        self.grade = "A"
        self.grade_date = "10/28/2015"
        self.action = "Violations were cited in the following area(s)."
        self.violation_description = "Short description of violation goes here."
        self.score = "8"
        self.csv_obj = {
            "BUILDING": self.building_number,
            "CRITICAL FLAG": self.critical,
            "DBA": self.restaurant_name,
            "INSPECTION DATE": self.inspection_date,
            "CUISINE DESCRIPTION": self.cuisine,
            "ZIPCODE": self.zip_code,
            "VIOLATION CODE": self.violation_code,
            "INSPECTION TYPE": self.inspection_type,
            "BORO": self.borough,
            "PHONE": self.phone,
            "RECORD DATE": "05/06/2017",
            "STREET": self.street_name,
            "CAMIS": self.registration_number,
            "GRADE": self.grade,
            "GRADE DATE": self.grade_date,
            "ACTION": self.action,
            "VIOLATION DESCRIPTION": self.violation_description,
            "SCORE": self.score
        }


class ExtractRestaurantTestCases(ExtractTestCases):
    def test_borough_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["borough"], self.borough)

    def test_building_number_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["building_number"], self.building_number)

    def test_cuisine_type_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["cuisine"], self.cuisine)

    def test_restaurant_name_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["name"], self.restaurant_name)

    def test_phone_number_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["phone"], self.phone)

    def test_registration_number_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["registration_number"], self.registration_number)

    def test_street_name_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["street_name"], self.street_name)

    def test_zip_code_is_extracted(self):
        restaurant_data = extract_restaurant_data(self.csv_obj)
        self.assertEqual(restaurant_data["zip_code"], self.zip_code)


class ExtractInspectionTestCases(ExtractTestCases):
    def test_inspection_data_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["date"], self.inspection_date)

    def test_action_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["action"], self.action)

    def test_violation_code_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["violation_code"], self.violation_code)

    def test_violation_description_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["violation_description"], self.violation_description)

    def test_critical_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["critical"], self.critical)

    def test_score_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["score"], self.score)

    def test_inspection_type_is_extracted(self):
        inspection_data = extract_inspection_data(self.csv_obj)
        self.assertEqual(inspection_data["check_type"], self.inspection_type)


class ExtractGradeTestCases(ExtractTestCases):
    def test_grade_is_extracted(self):
        grade_data = extract_grade_data(self.csv_obj)
        self.assertEqual(grade_data["score"], self.grade)

    def test_grade_date_is_extracted(self):
        grade_data = extract_grade_data(self.csv_obj)
        self.assertEqual(grade_data["date"], self.grade_date)


class TransformTestCases(ExtractTestCases):
    def setUp(self):
        super(TransformTestCases, self).setUp()
        self.restaurant_data = extract_restaurant_data(self.csv_obj)
        self.inspection_data = extract_inspection_data(self.csv_obj)
        self.grade_data = extract_grade_data(self.csv_obj)


class TransformRestaurantTestCases(TransformTestCases):
    def test_transform_removes_building_number(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertIsNone(self.restaurant_data.get("building_number"))

    def test_transform_removes_street_name(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertIsNone(self.restaurant_data.get("street_name"))

    def test_transform_adds_street(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertEqual(self.restaurant_data["street"], "{} {}".format(self.building_number, self.street_name))

    def test_transform_borough_to_lowercase(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertEquals(self.restaurant_data.get("borough"), self.borough.lower())

    def test_transform_zip_code_to_integer(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertEquals(self.restaurant_data.get("zip_code"), int(self.zip_code))

    def test_raises_transform_exception_for_invalid_zip_code(self):
        self.restaurant_data["zip_code"] = "N/A"
        self.assertRaises(TransformException, transform_restaurant_data, self.restaurant_data)

    def test_transform_phone_number_to_integer(self):
        self.restaurant_data["phone"] = "__________"
        transform_restaurant_data(self.restaurant_data)
        self.assertIsNone(self.restaurant_data.get("phone"))

    def test_transform_invalid_phone_number_to_none(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertEquals(self.restaurant_data.get("phone"), int(self.phone))

    def test_transform_registration_number_to_integer(self):
        transform_restaurant_data(self.restaurant_data)
        self.assertEquals(self.restaurant_data.get("registration_number"), int(self.registration_number))


class TransformInspectionTestCases(TransformTestCases):
    def test_transform_critical_to_false(self):
        transform_inspection_data(self.inspection_data)
        self.assertFalse(self.inspection_data.get("critical"))

    def test_transform_critical_to_true(self):
        self.inspection_data["critical"] = "Critical"
        transform_inspection_data(self.inspection_data)
        self.assertTrue(self.inspection_data.get("critical"))

    def test_transform_date_to_date_object(self):
        transform_inspection_data(self.inspection_data)
        self.assertEqual(self.inspection_data.get("date"), datetime.strptime(self.inspection_date, "%m/%d/%Y"))

    def test_transform_non_zero_padded_date_to_date_object(self):
        self.inspection_date = "1/1/1990"
        self.inspection_data["date"] = self.inspection_date
        transform_inspection_data(self.inspection_data)
        self.assertEqual(self.inspection_data.get("date"), datetime.strptime(self.inspection_date, "%m/%d/%Y"))

    def test_transform_score_to_integer(self):
        transform_inspection_data(self.inspection_data)
        self.assertEqual(self.inspection_data.get("score"), int(self.inspection_data.get("score")))

    def test_transform_empty_string_score_to_none(self):
        self.inspection_data["score"] = ""
        transform_inspection_data(self.inspection_data)
        self.assertIsNone(self.inspection_data.get("score"))


class TransformGradeTestCases(TransformTestCases):
    def test_transform_grade_a_to_integer(self):
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data["score"], 1)

    def test_transform_grade_b_to_integer(self):
        self.grade_data["score"] = "B"
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data["score"], 2)

    def test_transform_grade_c_to_integer(self):
        self.grade_data["score"] = "C"
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data["score"], 3)

    def test_transform_grade_z_to_integer(self):
        self.grade_data["score"] = "Z"
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data["score"], 26)

    def test_raises_transform_exception_for_empty_string_grade(self):
        self.grade_data["score"] = ""
        self.assertRaises(TransformException, transform_grade_data, self.grade_data)

    def test_raises_transform_exception_for_not_yet_graded(self):
        self.grade_data["score"] = "Not Yet Graded"
        self.assertRaises(TransformException, transform_grade_data, self.grade_data)

    def test_transform_date_to_date_object(self):
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data.get("date"), datetime.strptime(self.grade_date, "%m/%d/%Y"))

    def test_transform_non_zero_padded_date_to_date_object(self):
        self.grade_date = "1/1/1990"
        self.grade_data["date"] = self.grade_date
        transform_grade_data(self.grade_data)
        self.assertEqual(self.grade_data.get("date"), datetime.strptime(self.grade_date, "%m/%d/%Y"))

    def test_returns_false_for_empty_string_date(self):
        self.grade_data["date"] = ""
        self.assertRaises(TransformException, transform_grade_data, self.grade_data)


class LoadTestCases(TransformTestCases):
    def setUp(self):
        super(LoadTestCases, self).setUp()
        transform_restaurant_data(self.restaurant_data)
        transform_inspection_data(self.inspection_data)
        transform_grade_data(self.grade_data)
