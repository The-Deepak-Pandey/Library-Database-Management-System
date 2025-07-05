import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Database configuration
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def connect():
    return mysql.connector.connect(**DB_CONFIG)

def basic_operations_menu():
    print("\nBasic Operations:")
    print("1. Add new book")
    print("2. Issue book")
    print("3. Return book")
    print("4. Delete book")
    print("5. Search books by title")
    choice = input("Select option: ")

    conn = connect()
    cursor = conn.cursor()
    try:
        if choice == '1':
            isbn = input("ISBN: ")
            title = input("Title: ")
            category = input("Category: ")
            rental_price = float(input("Rental price: "))
            author = input("Author: ")
            publisher = input("Publisher: ")
            cursor.execute("""
                INSERT INTO books(isbn, book_title, category, rental_price, status, author, publisher)
                VALUES (%s, %s, %s, %s, 'yes', %s, %s)
            """, (isbn, title, category, rental_price, author, publisher))
            conn.commit()
            print("Book added successfully!")
        elif choice == '2':
            issued_id = input("Issued ID: ")
            member_id = input("Member ID: ")
            book_isbn = input("Book ISBN: ")
            emp_id = input("Employee ID: ")
            cursor.execute("""
                INSERT INTO issued_status(issued_id, issued_member_id, issued_date, issued_book_isbn, issued_emp_id)
                VALUES (%s, %s, CURDATE(), %s, %s)
            """, (issued_id, member_id, book_isbn, emp_id))
            cursor.execute("UPDATE books SET status = 'no' WHERE isbn = %s", (book_isbn,))
            conn.commit()
            print("Book issued successfully!")
        elif choice == '3':
            return_id = input("Return ID: ")
            issued_id = input("Issued ID: ")
            quality = input("Book quality: ")
            cursor.execute("""
                INSERT INTO return_status(return_id, issued_id, return_date, book_quality)
                VALUES (%s, %s, CURDATE(), %s)
            """, (return_id, issued_id, quality))
            cursor.execute("""
                UPDATE books SET status = 'yes'
                WHERE isbn = (SELECT issued_book_isbn FROM issued_status WHERE issued_id = %s)
            """, (issued_id,))
            conn.commit()
            print("Book returned successfully!")
        elif choice == '4':
            isbn = input("Book ISBN to delete: ")
            cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
            conn.commit()
            print("Book deleted successfully!")
        elif choice == '5':
            keyword = input("Enter title keyword to search: ")
            cursor.execute("SELECT * FROM books WHERE book_title LIKE %s", ('%' + keyword + '%',))
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        else:
            print("Invalid choice.")
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Database connection module ready")
