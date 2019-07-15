# Overview
Here is my third project for the "Full Stack Web Developer Nanodegree".

The objective of this project is to develop reporting tool made with python that query a database and displays the correct answers to each of the questions.
This project follows the PIP8 Python standard.

## Installation Requirements
To run correctly this project you will need:
1. Python
2. psycopg module
3. PostgreSQL
4. [newsdata - Database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
5. VirtualBox
6. Vagrant

### Setup

For this project, is needed to clone this [repo](https://github.com/udacity/fullstack-nanodegree-vm), this repo contains the files we will need to execute this project, including the database and the needed libraries. To have the exact same setup, you must:

Navigate to the vagrant subdirectory and type `vagrant up`. In the first time, it will download the virtual machine and install it on your computer. After the download and installation, to access your new virtual machine, type `vagrant ssh`.

Download and place the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) into the vagrant directory inside the repository folder. Use `psql -d news -f newsdata.sql` to setup the database.

### Database Structure and Functions
This database contains three tables, Authors, Articles and Log. This program will execute three SQL scripts to answer these three questions:
```
QUESTION_1 = "1. What are the most popular three articles of all time?"
QUESTION_2 = "2. Who are the most popular article authors of all time?"
QUESTION_3 = "3. On which days did more than 1% of requests lead to errors?"

QUERY_QUESTION_1 = (
        "SELECT title, "
        "	number_views "
        "FROM articles_views "
        "ORDER BY number_views DESC limit 3;"
    )

    QUERY_QUESTION_2 = (
        "SELECT a.name, "
        "	sum(b.number_views) AS number_views "
        "FROM authors a "
        "INNER JOIN articles_views b ON a.id = b.author "
        "GROUP BY a.name "
        "ORDER BY number_views DESC;"
    )

    QUERY_QUESTION_3 = (
        "SELECT to_char(log_date, 'FMMonth dd, yyyy'), "
        "	error_per_day "
        "FROM percent_errors "
        "WHERE error_per_day > 1.0;"
    )
``` 

### Run

To run your script: `python <script_name>.py` while logged into your development environment, assuming that it has all the requirements correctly installed.

After the program runs, it will show up in terminal the results and create a log file called lognews.txt.
