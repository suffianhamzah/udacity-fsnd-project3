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
$ git clone git@github.com:suffianhamzah/udacity-fsnd-project3.git
```

#### Install PostgreSQL
Please visit the official [PostgreSQL download page](https://www.postgresql.org/download/) to download and install PostgreSQL

#### Installing psycopg2
This project uses a python module called 'pyscopg2'. You will need to install it as a dependency using `pip`
```
pip install psycopg2
```

#### Getting the data for the database:
Please download the data from this [link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). It is a .zip file containing the sql file with schemas and the data itself.

#### Create database from the .sql file
Once you have downloaded the data, you can load your data into your database.
Run the command ```psql -d news -f newsdata.sql.```, where:
* ```psql``` - the PostgreSQL command line tool
* ```-d news``` = connect the database named news
* ```-f newsdata.sql``` = source of schema and data population for the news database
# Usage

To run this project, type: ```python reporting.py```