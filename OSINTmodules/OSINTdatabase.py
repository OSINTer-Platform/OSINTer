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

# Function for writting OG tags to database
def writeOGTagsToDB(connection, OGTags, tableName):
    # Making sure the tablename is in all lowercase
    tableName = tableName.lower()
    # List to hold all the urls that haven't been scraped and saved in the database before so the whole article can be scraped
    newUrls = list()
    with connection.cursor() as cur:
        for newsSite in OGTags:
            # Looping through each collection of tags
            for tags in OGTags[newsSite]:
                # Checking if the article is already stored in the database using the URL as that is probably not going to change and is uniqe
                cur.execute("SELECT exists (SELECT 1 FROM {} WHERE url = %s);".format(tableName), (tags['url'],))
                if cur.fetchall()[0][0] == False:
                    # Adding the url to list of new articles since it was not found in the database
                    newUrls.append(tags['url'])
                    insertQuery = "INSERT INTO {} (title, description, url, image_url, profile) VALUES (%s, %s, %s, %s, %s);".format(tableName)
                    insertParameters = (tags['title'], tags['description'], tags['url'], tags['image'], newsSite)
                    cur.execute(insertQuery, insertParameters)
    connection.commit()
    # Return the list of urls not already in the database so they can be scraped
    return newUrls
