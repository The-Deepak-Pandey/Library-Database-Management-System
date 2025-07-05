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

def run_task(task_num):
    conn = connect()
    cursor = conn.cursor()
    try:
        if task_num == '1':
            cursor.execute("""
                INSERT INTO books(isbn, book_title, category, rental_price, status, author, publisher)
                VALUES ('978-1-60129-456-2', 'To Kill a Mockingbird', 'Classic', 6.00, 'yes', 'Harper Lee', 'J.B. Lippincott & Co.')
            """)
            conn.commit()
            cursor.execute("SELECT * FROM books")
        elif task_num == '2':
            cursor.execute("UPDATE members SET member_address = '125 Main St' WHERE member_id = 'C101'")
            conn.commit()
            cursor.execute("SELECT * FROM members")
        elif task_num == '3':
            cursor.execute("DELETE FROM issued_status WHERE issued_id = 'IS121'")
            conn.commit()
            cursor.execute("SELECT * FROM issued_status")
        elif task_num == '4':
            cursor.execute("SELECT * FROM issued_status WHERE issued_emp_id = 'E101'")
        elif task_num == '5':
            cursor.execute("""
                SELECT ist.issued_emp_id, e.emp_name
                FROM issued_status ist
                JOIN employees e ON e.emp_id = ist.issued_emp_id
                GROUP BY ist.issued_emp_id, e.emp_name
                HAVING COUNT(ist.issued_id) > 1
            """)
        elif task_num == '6':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS book_cnts AS
                SELECT b.isbn, b.book_title, COUNT(ist.issued_id) as no_issued
                FROM books b
                JOIN issued_status ist ON ist.issued_book_isbn = b.isbn
                GROUP BY b.isbn, b.book_title
            """)
            conn.commit()
            cursor.execute("SELECT * FROM book_cnts")
        elif task_num == '7':
            cursor.execute("SELECT * FROM books WHERE category = 'Classic'")
        elif task_num == '8':
            cursor.execute("""
                SELECT b.category, SUM(b.rental_price), COUNT(*)
                FROM books b
                JOIN issued_status ist ON ist.issued_book_isbn = b.isbn
                GROUP BY b.category
            """)
        elif task_num == '9':
            cursor.execute("SELECT * FROM members WHERE reg_date >= CURDATE() - INTERVAL 180 DAY")
        else:
            print("Invalid task number.")
            return

        rows = cursor.fetchall()
        for row in rows:
            print(row)
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Database connection module ready")
