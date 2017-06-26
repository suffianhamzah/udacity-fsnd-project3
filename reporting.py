# Todo: Write 3 queries

import psycopg2


# Name of database we are going to connect to
DBNAME = 'news'


class dB(object):
    """A wrapper class for connecting to a database using pscyopg2

    This class handles the dB transactions and abstracts querying into
    functions based on CRUD (Create, Read, Update, and Delete).
    Currently, this class supports SELECT statements

    Attributes:
        db(obj): dB connection object instantiated from psycopg2
        cursor(obj): cursor object instantiated from db.cursor()

    """

    def __init__(self, DBNAME):
        """Initializes the DB connection"""
        self.db = psycopg2.connect(database=DBNAME)
        self.cursor = self.db.cursor()

    def get_query(self, sql_statement):
        """Executes SELECT query and returns results.

        Parameters:
            sql_statement (str): a valid SELECT statement to retrieve
                                 data

        Returns:
            A list containing 0 or more results of the query

        Raises:
            psycopg2.ProgrammingError: Incorrect statements will be raised
                                       and connection rolled back
        """
        try:
            self.cursor.execute(sql_statement)
        except psycopg2.ProgrammingError as error:
            print(error)
            self.db.rollback()
            return None

        return self.cursor.fetchall()

    def close(self):
        """Closes the db connection"""
        self.db.close()


def print_report(results, header, value_name):
    """Formats the sql results to format 'name' - number of value

    Example of output:
        Here are the results for the number of chickens in a farm!
        Green farm -- 5200 chickens
        Blue farm -- 10000 chickens
    """
    print("Here are the results for the {header}!".format(header=header))
    for text, value in results:
        print("{text} -- {value} {value_name}"
              .format(text=text, value=value, value_name=value_name))
    print("\n")


def get_most_popular_articles():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("select articles.title,count(*) as views "
                   "from articles "
                   "join log "
                   "on '/article/' || articles.slug = log.path "
                   "group by articles.title "
                   "order by views desc limit 3;")
    return cursor.fetchall()
    db.close()


def get_author_views_all_time():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("select authors.name, count(*) as views "
                   "from authors, articles, log "
                   "where authors.id = articles.author "
                   "and '/article/' || articles.slug = log.path "
                   "group by authors.name "
                   "order by views desc;")
    return cursor.fetchall()
    db.close()


def get_log_error():
    """
    gets the percentage -> created two views
    create view requestsuccess as
        select date_trunc('day',time) as date,
        count(*) as num
        from log
        where status = '200 OK'
        group by date
        order by num;
    """
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute(
        "select date, percentage::numeric(2,1) "
        "from (select time::date as date, "
        "sum(case when status != '200 OK' then 1 else 0 end) / "
        "sum(case when status = '200 OK' then 1 else 0 end)::float * "
        "100 as percentage "
        "from log group by date) as requesterrorpercentage "
        "where percentage::numeric(2,1) > 1;")
    return cursor.fetchall()
    db.close()


def main():
    # Initializes a DB object
    my_DB = dB(DBNAME)

    # Store sql results in variables to be used later
    articles = my_DB.get_query(
        "select articles.title,count(*) as views "
        "from articles "
        "join log "
        "on '/article/' || articles.slug = log.path "
        "group by articles.title "
        "order by views desc limit 3;")

    authors = my_DB.get_query(
        "select authors.name, count(*) as views "
        "from authors, articles, log "
        "where authors.id = articles.author "
        "and '/article/' || articles.slug = log.path "
        "group by authors.name "
        "order by views desc;")

    logs = my_DB.get_query(
        "select date, percentage::numeric(2,1) "
        "from (select time::date as date, "
        "sum(case when status != '200 OK' then 1 else 0 end) / "
        "sum(case when status = '200 OK' then 1 else 0 end)::float * "
        "100 as percentage "
        "from log group by date) as requesterrorpercentage "
        "where percentage > 1;")

    # Print the results
    print_report(articles, "top 3 most popular articles of all time!", "views")
    print_report(authors, "most popular article authors of all time", "views")
    print_report(logs,
                 "days where more than 1% of requests lead to errors",
                 "% errors")

    # Close db connection
    my_DB.close()


if __name__ == '__main__':
    main()
