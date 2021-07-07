#!/usr/bin/python3

# Used for creating a connection to the database
import psycopg2

from OSINTmodules import *

postgresqlPassword = ""


def main():
    # Connecting to the database
    conn = psycopg2.connect("dbname=osinter user=postgres password=" + postgresqlPassword)

    scrambledOGTags = OSINTtags.scrambleOGTags(OSINTdatabase.requestOGTagsFromDB(conn, 'articles'))

    OSINTfiles.constructArticleOverview(scrambledOGTags)


main()
