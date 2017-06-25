# Todo: Write 3 queries

import psycopg2


# Name of database we are going to connect to
DBNAME = 'news'


def print_report(results, header, value_name):
    """Formats the sql results to format 'name' - number of value"""
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
    cursor.execute("select date, percentage::numeric(2,1) "
                   "from requesterrorpercentage where percentage > 1;")
    select * from (select time::date as date, sum(case when status != '200 OK' then 1 else 0 end)/ sum(case when status = '200 OK' then 1 else 0 end)::float * 100 as percentage from log group by date) as test  where percentage > 1;
    return cursor.fetchall()
    db.close()


def main():
    # Store sql results in variables to be used later
    articles = get_most_popular_articles()
    authors = get_author_views_all_time()
    logs = get_log_error()
    # Print the results
    print_report(articles, "top 3 most popular articles of all time!", "views")
    print_report(authors, "most popular article authors of all time", "views")
    print_report(logs,
                 "days where more than 1% of requests lead to errors",
                 "% errors")


if __name__ == '__main__':
    main()
