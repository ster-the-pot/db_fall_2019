import mysql.connector as mysql
import csvparse


mydb = mysql.connect(
    host="localhost",
    user="root",
    passwd="2112.Bruins.Chase.98.",
    database="biology"
)

cursor = mydb.cursor()

csvparse.csvInput("exptest.csv", cursor)
