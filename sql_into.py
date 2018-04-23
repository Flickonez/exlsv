import MySQLdb

try:
    conn = MySQLdb.connect(host="sql11.freesqldatabase.com", user="sql11200147", 
                           passwd="f5Tf1uLxWY", db="sql11200147")
except MySQLdb.Error as err:
    print("Connection error: {}".format(err))
    conn.close()

count_rating(conn)
