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
        elif task_num == '10':
            cursor.execute("""
                SELECT e1.*, b.manager_id, e2.emp_name as manager
                FROM employees e1
                JOIN branch b ON b.branch_id = e1.branch_id
                JOIN employees e2 ON b.manager_id = e2.emp_id
            """)
        elif task_num == '11':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books_price_greater_than_seven AS
                SELECT * FROM books WHERE rental_price > 7
            """)
            conn.commit()
            cursor.execute("SELECT * FROM books_price_greater_than_seven")
        elif task_num == '12':
            cursor.execute("""
                SELECT DISTINCT ist.issued_book_name
                FROM issued_status ist
                LEFT JOIN return_status rs ON ist.issued_id = rs.issued_id
                WHERE rs.return_id IS NULL
            """)
        elif task_num == '13':
            cursor.execute("""
                SELECT ist.issued_member_id, m.member_name, bk.book_title, ist.issued_date,
                       DATEDIFF(CURDATE(), ist.issued_date) as over_due_days
                FROM issued_status ist
                JOIN members m ON m.member_id = ist.issued_member_id
                JOIN books bk ON bk.isbn = ist.issued_book_isbn
                LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
                WHERE rs.return_id IS NULL AND DATEDIFF(CURDATE(), ist.issued_date) > 30
            """)
        elif task_num == '14':
            cursor.execute("""
                UPDATE books
                SET status = 'yes'
                WHERE isbn IN (
                    SELECT issued_book_isbn FROM issued_status
                    WHERE issued_id IN (SELECT issued_id FROM return_status)
                )
            """)
            conn.commit()
            cursor.execute("SELECT * FROM books")
        elif task_num == '15':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS branch_reports AS
                SELECT b.branch_id, b.manager_id,
                       COUNT(ist.issued_id) as number_book_issued,
                       COUNT(rs.return_id) as number_of_book_return,
                       SUM(bk.rental_price) as total_revenue
                FROM issued_status ist
                JOIN employees e ON e.emp_id = ist.issued_emp_id
                JOIN branch b ON e.branch_id = b.branch_id
                LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
                JOIN books bk ON ist.issued_book_isbn = bk.isbn
                GROUP BY b.branch_id, b.manager_id
            """)
            conn.commit()
            cursor.execute("SELECT * FROM branch_reports")
        elif task_num == '16':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS active_members AS
                SELECT * FROM members
                WHERE member_id IN (
                    SELECT DISTINCT issued_member_id
                    FROM issued_status
                    WHERE issued_date >= CURDATE() - INTERVAL 2 MONTH
                )
            """)
            conn.commit()
            cursor.execute("SELECT * FROM active_members")
        elif task_num == '17':
            cursor.execute("""
                SELECT e.emp_name, b.branch_name, COUNT(ist.issued_id) as no_book_issued
                FROM issued_status ist
                JOIN employees e ON e.emp_id = ist.issued_emp_id
                JOIN branch b ON e.branch_id = b.branch_id
                GROUP BY e.emp_name, b.branch_name
                ORDER BY no_book_issued DESC LIMIT 3
            """)
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

def predefined_tasks_menu():
    print("\nPredefined Tasks / Reports:")
    print("1: Add new book (Task 1)")
    print("2: Update member address")
    print("3: Delete issued status record")
    print("4: List books issued by employee")
    print("5: Members who issued more than one book")
    print("6: Create summary table (book_cnts)")
    print("7: Retrieve books in category 'Classic'")
    print("8: Total rental income by category")
    print("9: Members registered in last 180 days")
    print("10: Employees with branch manager info")
    print("11: Create table of books price > $7")
    print("12: Books not yet returned")
    print("13: Members with overdue books (>30 days)")
    print("14: Update book status on return")
    print("15: Branch performance report")
    print("16: Create active members table")
    print("17: Top 3 employees by books processed")
    print("b: Back to main menu")
    choice = input("Enter task number: ")
    if choice.lower() != 'b':
        run_task(choice)

def main():
    while True:
        print("\nLibrary CLI - Main Menu:")
        print("1. Basic Operations")
        print("2. Predefined Tasks / Reports")
        print("q. Quit")
        choice = input("Select option: ")
        if choice == '1':
            basic_operations_menu()
        elif choice == '2':
            predefined_tasks_menu()
        elif choice.lower() == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()