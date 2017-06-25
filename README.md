Project 3: Log analysis report
====================================
This project is about getting answers to these three questions by querying data from a database. The questions are:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

# Installation
First, either clone or download the project code from this repo:

#### Cloning using SSH or HTTPS
```
$ git clone <https>
```

#### Install PostgreSQL
Please visit the official [PostgreSQL download page](https://www.postgresql.org/download/) to download and install PostgreSQL

#### Installing psycopg2
This project uses a python module called 'pyscopg2'. You will need to install it as a dependency using `pip`
```
pip install psycopg2
```

#### Create database from schema sql

#### Create views used for SQL queries
This project uses a custom view called ```requesterrorpercentage```. You will need to use ```psql```,
and then create the view using the SQL statement below:
```SQL
CREATE VIEW requesterrorpercentage AS
SELECT time::date AS date,
    (
        SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) /
        SUM(CASE when status = '200 OK' THEN 1 ELSE 0 END)::FLOAT *
        100
    ) AS percentage
FROM log
GROUP BY date;
```
This view was made with reference to this [stackoverflow Q & A](https://stackoverflow.com/questions/12359054/sql-group-by-generate-multiple-aggregate-columns-from-single-column)

# Usage

To run this project, type: ```python reporting.py```