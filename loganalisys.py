#!/usr/bin/env python
import psycopg2
import os


class DBCursor:
    """ This class creates the connection to database and handles the
      connection
    """

    def __init__(self):

        self.connection = None
        self.cursor = None

    def __enter__(self):

        try:
            self.connection = psycopg2.connect("dbname=news")
        except psycopg2.Error as e:
            print("Unable to connect to the database")
            print(e.pgerror)
            print(e.diag.message_detail)
            sys.exit(1)

        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_value:
            print "Error executing query!"

        self.connection.close()

        return True


class LogAnalysis:
    # Log Analysis questions
    QUESTION_1 = "1. What are the most popular three articles of all time?"
    QUESTION_2 = "2. Who are the most popular article authors of all time?"
    QUESTION_3 = (
        "3. On which days did more than 1% of requests lead to errors?"
    )

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

    def __init__(self):
        """
        Initialize answer_one, answer_two and answer_three as None
        """
        self.answer_one = None
        self.answer_two = None
        self.answer_three = None

    def execute_query(self, query):
        answer = ""
        with DBCursor() as cursor:
            cursor.execute(query)
            answer = cursor.fetchall()
        return answer

    def get_question_one(self):
        return self.QUESTION_1

    def get_answer_one(self):
        self.answer_one = self.execute_query(self.QUERY_QUESTION_1)

        writing_log(self.QUESTION_1)
        writing_log("\n".join(
                '"%s" - %s views' % tupl for tupl in self.answer_one)
            )

        return "\n".join('"%s" - %s views' % tupl for tupl in self.answer_one)

    def get_question_two(self):
        return self.QUESTION_2

    def get_answer_two(self):
        self.answer_two = self.execute_query(self.QUERY_QUESTION_2)
        writing_log(self.QUESTION_2)
        writing_log("\n".join(
                '%s - %s views' % tupl for tupl in self.answer_two)
            )
        return "\n".join(
                '%s - %s views' % tupl for tupl in self.answer_two
            )

    def get_question_three(self):
        return self.QUESTION_3

    def get_answer_three(self):

        self.answer_three = self.execute_query(self.QUERY_QUESTION_3)
        writing_log(self.QUESTION_3)
        writing_log("\n".join(
            '%s - %s%% errors' % tupl for tupl in self.answer_three
        ))
        return "\n".join(
            '%s - %s%% errors' % tupl for tupl in self.answer_three
        )


def main():

    log = LogAnalysis()

    # Print Header with version
    print "\n*** Log Analysis reporting tool of the Newsdata DB - V 1.0 ***\n"

    print log.get_question_one() + "\n"
    print log.get_answer_one()
    print "\n"

    print log.get_question_two() + "\n"
    print log.get_answer_two()
    print "\n"

    print log.get_question_three() + "\n"
    print log.get_answer_three()
    print "\n"

    if os.path.isfile("lognews.txt"):
        print "Logfile write in catalog/"


def writing_log(message):

    if os.path.isfile("lognews.txt"):
        log_file = open("lognews.txt", "a")

    else:
        log_file = open("lognews.txt", "w")

    if os.stat("lognews.txt").st_size == 0:
        log_file.write("Log Analysis reporting tool of the Newsdata BD-V1.0")
        log_file.write("\n-------------------------------------\n")
        log_file.write(message)

    else:
        log_file.write("\n")
        log_file.write(message)

    log_file.close()


if __name__ == '__main__':
    main()
