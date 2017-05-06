# Requirements
Using [DOHMH New York City Restaurant Inspection Results](https://nycopendata.socrata.com/api/views/xx67-kt59/rows.csv?accessType=DOWNLOAD) complete the following:
- Create an ETL to ingest the result set.
- Get the top 10 Thai restaurants with a health rating of B or higher.
- Create a web front end to display the results.

# Solution
## ETL Schema justification
### Restaurant
- `registration_number` - Each restaurant gets a unique registration number assigned to them by the city.
- `name` - All restaurants should have a name that they display on their storefront.
- Address - The physical location of the establishment.
    - `street_address`
    - `borough`
    - `zip_code`
- `phone_number` - Restaurants need a phone line to accept takeout orders.
- `cuisine` - Indicates the type of food the restaurant serve.

### Inspection
- `restaurant` - The restaurant this inspection belongs to.
- `check_type` - The type of inspection that was performed.
- `grade` - The letter rating the Department of Health assigned during the inspection.
- `grade_date` - The date the grade was assigned.
- `score` - A number representing how many health violations a restaurant has.
- `date` - The date the inspection was conducted.
- `violation_code` - Code representing the violation type.
- `violation_description` - A brief description of the violation type.
- `critical` - A flag indicating the severity of the violation.
- `action` - Action that the Department of Health took as a result of the inspection.

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
GRADE - Inspection.grade
GRADE DATE - Inspection.date
RECORD DATE - NOT USED
INSPECTION TYPE - Inspection.check_type
```

### SQL statement for the top 10 Thai restaurants.
TODO

# Web Application
## Deploying to Heroku
- Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).
- `heroku create`
- `git push heroku master`

# TODO
- Run through the [Django production checklist](https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/).