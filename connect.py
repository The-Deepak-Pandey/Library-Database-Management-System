import mysql.connector

# replace with your actual database info
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="library"
)

print("✅ Connected to database!")

conn.close()
