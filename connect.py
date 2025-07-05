import mysql.connector
import os


# replace with your actual database info
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=os.getenv("SQL_PASSWORD"),
    database="library"
)

print("✅ Connected to database!")

conn.close()
