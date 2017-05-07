# Demo
[Link](https://quiet-anchorage-87455.herokuapp.com/)

# Requirements

Using [DOHMH New York City Restaurant Inspection Results](https://nycopendata.socrata.com/api/views/xx67-kt59/rows.csv?accessType=DOWNLOAD) complete the following:
- Create an ETL to ingest the result set.
- Get the top 10 Thai restaurants with a health rating of B or higher.
- Create a web front end to display the results.

# Solution

## Table Creation

```mysql
BEGIN;
--
-- Create model Grade
--
CREATE TABLE "restaurants_grade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "score" integer NOT NULL);
--
-- Create model Inspection
--
CREATE TABLE "restaurants_inspection" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action" varchar(255) NOT NULL, "check_type" varchar(255) NOT NULL, "critical" bool NOT NULL, "date" date NOT NULL, "score" smallint NULL, "violation_code" varchar(3) NOT NULL,
 "violation_description" text NOT NULL);
--
-- Create model Restaurant
--
CREATE TABLE "restaurants_restaurant" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "borough" varchar(13) NOT NULL, "cuisine" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "phone_number" bigint NULL, "registration_number" integer unsigned NOT NULL UNIQU
E, "street_address" varchar(255) NOT NULL, "zip_code" smallint unsigned NOT NULL);
--
-- Add field restaurant to inspection
--
ALTER TABLE "restaurants_inspection" RENAME TO "restaurants_inspection__old";
CREATE TABLE "restaurants_inspection" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "action" varchar(255) NOT NULL, "check_type" varchar(255) NOT NULL, "critical" bool NOT NULL, "date" date NOT NULL, "score" smallint NULL, "violation_code" varchar(3) NOT NULL,
 "violation_description" text NOT NULL, "restaurant_id" integer NOT NULL REFERENCES "restaurants_restaurant" ("id"));
INSERT INTO "restaurants_inspection" ("score", "restaurant_id", "violation_code", "date", "critical", "action", "violation_description", "id", "check_type") SELECT "score", NULL, "violation_code", "date", "critical", "action", "violation_description", "id", "check
_type" FROM "restaurants_inspection__old";
DROP TABLE "restaurants_inspection__old";
CREATE INDEX "restaurants_inspection_restaurant_id_ef5882cc" ON "restaurants_inspection" ("restaurant_id");
--
-- Add field restaurant to grade
--
ALTER TABLE "restaurants_grade" RENAME TO "restaurants_grade__old";
CREATE TABLE "restaurants_grade" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date" date NOT NULL, "score" integer NOT NULL, "restaurant_id" integer NOT NULL REFERENCES "restaurants_restaurant" ("id"));
INSERT INTO "restaurants_grade" ("date", "restaurant_id", "score", "id") SELECT "date", NULL, "score", "id" FROM "restaurants_grade__old";
DROP TABLE "restaurants_grade__old";
CREATE INDEX "restaurants_grade_restaurant_id_37d19abe" ON "restaurants_grade" ("restaurant_id");
COMMIT;
```

## ETL Script

[Source](/restaurants/etl.py)

## SQL statement for the top 10 Thai restaurants.

```mysql
SELECT DISTINCT "restaurants_restaurant"."borough", "restaurants_restaurant"."name", "restaurants_restaurant"."phone_number", "restaurants_restaurant"."registration_number", "restaurants_restaurant"."street_address", "restaurants_restaurant"."zip_code", "restaurants_grade"."score"
FROM "restaurants_restaurant"
INNER JOIN "restaurants_grade" ON ("restaurants_restaurant"."id" = "restaurants_grade"."restaurant_id")
WHERE ("restaurants_restaurant"."cuisine" = Thai AND "restaurants_grade"."score" <= 2)
ORDER BY "restaurants_grade"."score"
ASC LIMIT 10
```

## ETL Schema justification

### Restaurant

This model is needed because we need a representation for each restaurant.

- `registration_number` - Each restaurant gets a unique registration number assigned to them by the city.
- `name` - All restaurants should have a name that they display on their storefront.
- Address - The physical location of the establishment.
    - `street_address`
    - `borough`
    - `zip_code`
- `phone_number` - Most restaurants have an associated a phone line to accept takeout orders.
- `cuisine` - Indicates the type of food the restaurant serve.

### Inspection

This model is created because there can be multiple inspections on different dates per restaurant.

- `restaurant` - The restaurant this inspection belongs to.
- `check_type` - The type of inspection that was performed.
- `score` - A number representing how many health violations a restaurant has.
- `date` - The date the inspection was conducted.
- `violation_code` - Code representing the violation type.
- `violation_description` - A brief description of the violation type.
- `critical` - A flag indicating the severity of the violation.
- `action` - Action that the Department of Health took as a result of the inspection.


### Grade

This model is created because not every inspection has a grade and grades have their own dates. There can be history of grades for each restaurant.

- `restaurant` - The restaurant this inspection belongs to.
- `score` - The letter grade.
- `date` - The date the grade was assigned.

## Mapping the result set to the ETL Schemas.

- The `BUILDING` and `STREET` columsn will get combined into a single `street_address` column in the `Restaurant` table.
- The `RECORD DATE` column is not mapped because it is the date the data was entered into NYC Open Data's database and not related to any restaurant or inspection.
- The `GRADE` column is used even though the grade can usually be derived from the `SCORE` column, not every restaurant has been assigned a grade.
    ```
    A - < 14 violations
    B - < 28 violations
    C - >= 28 violations
    ```
```
CAMIS -> Restaurant.registration_number
DBA -> Restaurant.name
BORO -> Restaurant.borough
// BUILDING and STREET will be combined into a single field.
BUILDING -> Restaurant.street_address
STREET -> Restaurant.street_address
ZIPCODE -> Restaurant.zip_code
PHONE -> Restaurant.phone
CUISINE DESCRIPTION -> Restaurant.cuisine

INSPECTION DATE - Inspection.date
ACTION - Inspection.action
VIOLATION CODE - Inspection.violation_code
VIOLATION DESCRIPTION - Inspection.violation_description
CRITICAL FLAG - Inspection.critical
SCORE - Inspection.score
INSPECTION TYPE - Inspection.check_type

GRADE - GRADE.score
GRADE DATE - GRADE.date

RECORD DATE - NOT USED
```

# Web Application

## Running the ETL

```bash
python manage.py run_etl
```

## Deploying to Heroku

- Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
- Install the latest version of [Node](https://nodejs.org/en/download/).
- Make this repo the current directory.
- `npm run build`
- `heroku create`
- `git push heroku master`
- `heroku run python manage.py migrate`
- `heroku run python manage.py createsuperuser`

## Running tests

```bash
python manage.py test
```

# TODO

- Run through the [Django production checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/) and ensure the application is production ready.
- Make the load portion of the ETL atomic.
- Create an API for retrieving restaurant, inspection, and grade data.
- Incorporate React-Router to allow direct linking to a particular filter.
- Add views that dive into past inspections and grades.
- Add search and sorting in the restaurant table.