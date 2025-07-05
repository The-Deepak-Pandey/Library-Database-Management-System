import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# replace with your actual database info
conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"), 
    database=os.getenv("DB_NAME")
)

print("✅ Connected to database!")

conn.close()
