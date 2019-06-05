# This file connects to the MySQL DataBase

import mysql.connector

mydb = mysql.connector.connect(
		host = "localhost",
		user = "root",
		passwd = "admin"
	)

mycursor = mydb.cursor()

print(mycursor.execute("SHOW DATABASES"))