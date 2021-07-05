#!/usr/bin/python

def initiateArticleTable(connection):
    tableContentList = [
                            "id BIGSERIAL NOT NULL PRIMARY KEY",
                            "title VARCHAR(150) NOT NULL",
                            "description VARCHAR(350)",
                            "url VARCHAR(300) NOT NULL",
                            "image_url VARCHAR(300)",
                            "profile VARCHAR(30) NOT NULL"
                        ]
    createTable(connection, "articles", tableContentList)

# Function for creating new tables
def createTable(connection, tableName, tableContentList):
    # Opening new cursor that will automatically close when function is done
    with connection.cursor() as cur:
        # Checking if a table with the specified wanted name already exists
        cur.execute("SELECT to_regclass('public.{}');".format(tableName.lower()))
        results = cur.fetchall()
        if results[0][0] == None:
            # Creating the text used to specify the contents of the table
            tableContents = ", ".join([x for x in tableContentList])
            # Creating the table with the specified content
            cur.execute("CREATE TABLE {} ({});".format(tableName.lower(), tableContents))
            # Writing the changes to the database
            connection.commit()
        else:
            print("Table \"%s\" already exists, skipping it for now" % tableName.lower())
