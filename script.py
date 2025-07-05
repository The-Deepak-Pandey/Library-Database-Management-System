import mysql.connector
import os
from dotenv import load_dotenv
import time

load_dotenv()  # Load environment variables from .env file

# Database configuration
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def connect():
    """Establishes a connection to the MySQL database."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"\n--- DATABASE CONNECTION ERROR ---")
        print(f"Oops! Couldn't connect to the database: {err}")
        print("Please check your .env file and ensure the database is running.")
        print("Exiting application.")
        exit() # Exit if we can't connect to the database

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints a stylized ASCII art banner for the Library Management System."""
    clear_screen()
    print(r"""
██╗      ██╗██████╗ ██████╗  █████╗ ██████╗ ██╗    ██╗     ██████╗  █████╗ ████████╗ █████╗ ██████╗  █████╗ ███████╗███████╗   
██║      ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝     ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔════╝   
██║      ██║██████╔╝██████╔╝███████║██████╔╝ ╚████╔╝      ██║  ██║███████║   ██║   ███████║██████╔╝███████║███████╗█████╗     
██║      ██║██╔══██╗██╔══██╗██╔══██║██╔══██╗  ╚██╔╝       ██║  ██║██╔══██║   ██║   ██╔══██║██╔══██╗██╔══██║╚════██║██╔══╝     
███████╗██║██████╔╝██║  ██║██║  ██║██║  ██║  ██║         ██████╔╝██║  ██║   ██║   ██║  ██║██████╔╝██║  ██║███████║███████╗   
╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ╚═╝         ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝   
                                                                                                                    
                            ███╗   ███╗ █████╗ ███╗   ██╗ █████╗  ██████╗ ███████╗██████╗                            
                            ████╗ ████║██╔══██╗████╗  ██║██╔══██╗██╔════╝ ██╔════╝██╔══██╗                           
                            ██╔████╔██║███████║██╔██╗ ██║███████║██║  ███╗█████╗  ██████╔╝                           
                            ██║╚██╔╝██║██╔══██║██║╚██╗██║██╔══██║██║  ██║██╔══╝  ██╔══██╗                           
                            ██║ ╚═╝ ██║██║  ██║██║ ╚████║██║  ██║╚██████╔╝███████╗██║  ██║                           
                            ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝                           
""")
    print("\n" + "="*90) # Adjusted width for the new, wider banner
    print(f"{'Your Ultimate Solution for Managing Library Resources':^90}") # Updated tagline
    print("="*90 + "\n")
    # time.sleep(0.1)

def add_new_data_menu():
    """Menu for adding new data to various tables."""
    conn = None
    cursor = None
    try:
        conn = connect()
        if conn is None:
            return
        cursor = conn.cursor()

        while True:
            print_banner()
            print("--- ADD NEW DATA ---")
            print("Select a table to add data to:")
            print("1. Add a New Book")
            print("2. Add a New Member")
            print("3. Add a New Employee")
            print("4. Add a New Branch")
            print("5. Record a Book Issue")
            print("6. Record a Book Return")
            print("b. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip().lower()

            if choice == '1':
                print("\n--- ADD NEW BOOK ---")
                isbn = input("Enter ISBN (e.g., 978-1-23456-789-0): ").strip()
                title = input("Enter Book Title: ").strip()
                category = input("Enter Category (e.g., Fiction, Science, History): ").strip()
                while True:
                    try:
                        rental_price = float(input("Enter Rental Price (e.g., 5.99): ").strip())
                        if rental_price < 0:
                            print("Price cannot be negative. Please enter a valid amount.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input for price. Please enter a numerical value.")
                author = input("Enter Author's Name: ").strip()
                publisher = input("Enter Publisher: ").strip()

                cursor.execute("""
                    INSERT INTO books(isbn, book_title, category, rental_price, status, author, publisher)
                    VALUES (%s, %s, %s, %s, 'yes', %s, %s)
                """, (isbn, title, category, rental_price, author, publisher))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"'{title}' (ISBN: {isbn}) has been successfully added to the library.")

            elif choice == '2':
                print("\n--- ADD NEW MEMBER ---")
                member_id = input("Enter Member ID (e.g., M001): ").strip()
                member_name = input("Enter Member Name: ").strip()
                member_address = input("Enter Member Address: ").strip()
                reg_date = input("Enter Registration Date (YYYY-MM-DD): ").strip()
                
                cursor.execute("""
                    INSERT INTO members(member_id, member_name, member_address, reg_date)
                    VALUES (%s, %s, %s, %s)
                """, (member_id, member_name, member_address, reg_date))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"Member '{member_name}' (ID: {member_id}) has been successfully added.")

            elif choice == '3':
                print("\n--- ADD NEW EMPLOYEE ---")
                emp_id = input("Enter Employee ID (e.g., E001): ").strip()
                emp_name = input("Enter Employee Name: ").strip()
                position = input("Enter Position (e.g., Librarian, Assistant): ").strip()
                while True:
                    try:
                        salary = float(input("Enter Salary (e.g., 50000.00): ").strip())
                        if salary < 0:
                            print("Salary cannot be negative. Please enter a valid amount.")
                        else:
                            break
                    except ValueError:
                        print("Invalid input for salary. Please enter a numerical value.")
                branch_id = input("Enter Branch ID (e.g., B001): ").strip()

                cursor.execute("""
                    INSERT INTO employees(emp_id, emp_name, position, salary, branch_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (emp_id, emp_name, position, salary, branch_id))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"Employee '{emp_name}' (ID: {emp_id}) has been successfully added.")

            elif choice == '4':
                print("\n--- ADD NEW BRANCH ---")
                branch_id = input("Enter Branch ID (e.g., B001): ").strip()
                manager_id = input("Enter Manager ID (e.g., E001): ").strip()
                branch_address = input("Enter Branch Address: ").strip()
                contact_no = input("Enter Contact Number: ").strip()

                cursor.execute("""
                    INSERT INTO branch(branch_id, manager_id, branch_address, contact_no)
                    VALUES (%s, %s, %s, %s)
                """, (branch_id, manager_id, branch_address, contact_no))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"Branch '{branch_address}' (ID: {branch_id}) has been successfully added.")

            elif choice == '5':
                print("\n--- RECORD BOOK ISSUE ---")
                issued_id = input("Enter Issued ID (e.g., IS001): ").strip()
                issued_member_id = input("Enter Member ID: ").strip()
                issued_book_isbn = input("Enter Book ISBN: ").strip()
                issued_emp_id = input("Enter Employee ID (who issued): ").strip()

                # Optional: Get book title for 'issued_book_name' field
                cursor.execute("SELECT book_title FROM books WHERE isbn = %s", (issued_book_isbn,))
                book_title_result = cursor.fetchone()
                issued_book_name = book_title_result[0] if book_title_result else "Unknown Book"

                cursor.execute("""
                    INSERT INTO issued_status(issued_id, issued_member_id, issued_book_name, issued_date, issued_book_isbn, issued_emp_id)
                    VALUES (%s, %s, %s, CURDATE(), %s, %s)
                """, (issued_id, issued_member_id, issued_book_name, issued_book_isbn, issued_emp_id))
                cursor.execute("UPDATE books SET status = 'no' WHERE isbn = %s", (issued_book_isbn,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"Book '{issued_book_name}' (ISBN: {issued_book_isbn}) issued to Member '{issued_member_id}'.")

            elif choice == '6':
                print("\n--- RECORD BOOK RETURN ---")
                return_id = input("Enter Return ID (e.g., R001): ").strip()
                issued_id = input("Enter Issued ID (associated with the issued book): ").strip()
                
                # Fetch book ISBN and name from issued_status
                cursor.execute("SELECT issued_book_isbn, issued_book_name FROM issued_status WHERE issued_id = %s", (issued_id,))
                issue_info = cursor.fetchone()

                if not issue_info:
                    print("\n--- ERROR ---")
                    print(f"No issued record found for Issued ID '{issued_id}'. Cannot process return.")
                    input("\nPress Enter to continue...")
                    continue

                return_book_isbn = issue_info[0]
                return_book_name = issue_info[1]
                
                cursor.execute("""
                    INSERT INTO return_status(return_id, issued_id, return_book_name, return_date, return_book_isbn)
                    VALUES (%s, %s, %s, CURDATE(), %s)
                """, (return_id, issued_id, return_book_name, return_book_isbn))
                cursor.execute("UPDATE books SET status = 'yes' WHERE isbn = %s", (return_book_isbn,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                print(f"Book '{return_book_name}' (ISBN: {return_book_isbn}) associated with Issued ID '{issued_id}' has been successfully returned.")

            elif choice == 'b':
                break
            else:
                print("\n--- INVALID CHOICE ---")
                print("Please select a valid option (1-6 or 'b').")
            input("\nPress Enter to continue...")

    except mysql.connector.Error as err:
        print(f"\n--- DATABASE ERROR ---")
        print(f"An error occurred during the operation: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"Something went wrong: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def remove_data_menu():
    """Menu for removing data from various tables."""
    conn = None
    cursor = None
    try:
        conn = connect()
        if conn is None:
            return
        cursor = conn.cursor()

        while True:
            print_banner()
            print("--- REMOVE DATA ---")
            print("Select a table to remove data from:")
            print("1. Remove a Book")
            print("2. Remove a Member")
            print("3. Remove an Employee")
            print("4. Remove a Branch")
            print("5. Remove an Issued Record")
            print("6. Remove a Return Record")
            print("b. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip().lower()

            if choice == '1':
                print("\n--- REMOVE BOOK ---")
                isbn = input("Enter ISBN of the book to delete: ").strip()
                cursor.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Book with ISBN '{isbn}' has been successfully deleted.")
                else:
                    print(f"No book found with ISBN '{isbn}'.")

            elif choice == '2':
                print("\n--- REMOVE MEMBER ---")
                member_id = input("Enter Member ID to delete: ").strip()
                cursor.execute("DELETE FROM members WHERE member_id = %s", (member_id,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Member with ID '{member_id}' has been successfully deleted.")
                else:
                    print(f"No member found with ID '{member_id}'.")

            elif choice == '3':
                print("\n--- REMOVE EMPLOYEE ---")
                emp_id = input("Enter Employee ID to delete: ").strip()
                cursor.execute("DELETE FROM employees WHERE emp_id = %s", (emp_id,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Employee with ID '{emp_id}' has been successfully deleted.")
                else:
                    print(f"No employee found with ID '{emp_id}'.")

            elif choice == '4':
                print("\n--- REMOVE BRANCH ---")
                branch_id = input("Enter Branch ID to delete: ").strip()
                cursor.execute("DELETE FROM branch WHERE branch_id = %s", (branch_id,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Branch with ID '{branch_id}' has been successfully deleted.")
                else:
                    print(f"No branch found with ID '{branch_id}'.")

            elif choice == '5':
                print("\n--- REMOVE ISSUED RECORD ---")
                issued_id = input("Enter Issued ID to delete: ").strip()
                cursor.execute("DELETE FROM issued_status WHERE issued_id = %s", (issued_id,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Issued record with ID '{issued_id}' has been successfully deleted.")
                else:
                    print(f"No issued record found with ID '{issued_id}'.")

            elif choice == '6':
                print("\n--- REMOVE RETURN RECORD ---")
                return_id = input("Enter Return ID to delete: ").strip()
                cursor.execute("DELETE FROM return_status WHERE return_id = %s", (return_id,))
                conn.commit()
                print("\n--- SUCCESS! ---")
                if cursor.rowcount > 0:
                    print(f"Return record with ID '{return_id}' has been successfully deleted.")
                else:
                    print(f"No return record found with ID '{return_id}'.")

            elif choice == 'b':
                break
            else:
                print("\n--- INVALID CHOICE ---")
                print("Please select a valid option (1-6 or 'b').")
            input("\nPress Enter to continue...")

    except mysql.connector.Error as err:
        print(f"\n--- DATABASE ERROR ---")
        print(f"An error occurred during the operation: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"Something went wrong: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def display_data_menu():
    """Menu for displaying data from various tables."""
    conn = None
    cursor = None
    try:
        conn = connect()
        if conn is None:
            return
        cursor = conn.cursor()

        while True:
            print_banner()
            print("--- DISPLAY DATA ---")
            print("Select data to display:")
            print("1. Display Complete Data for a Table")
            print("2. Search Books by Title")
            print("b. Back to Main Menu")

            choice = input("\nEnter your choice: ").strip().lower()

            if choice == '1':
                print_banner()
                print("--- DISPLAY COMPLETE DATA ---")
                print("Select a table to display:")
                print("1. Branch")
                print("2. Employees")
                print("3. Members")
                print("4. Books")
                print("5. Issued Status")
                print("6. Return Status")
                print("b. Back to Display Data Menu")
                
                table_choice = input("\nEnter your choice: ").strip().lower()
                table_map = {
                    '1': ('branch', ['Branch ID', 'Manager ID', 'Address', 'Contact No']),
                    '2': ('employees', ['Employee ID', 'Name', 'Position', 'Salary', 'Branch ID']),
                    '3': ('members', ['Member ID', 'Name', 'Address', 'Registration Date']),
                    '4': ('books', ['ISBN', 'Title', 'Category', 'Rental Price', 'Status', 'Author', 'Publisher']),
                    '5': ('issued_status', ['Issued ID', 'Member ID', 'Book Name', 'Issue Date', 'Book ISBN', 'Employee ID']),
                    '6': ('return_status', ['Return ID', 'Issued ID', 'Book Name', 'Return Date', 'Book ISBN'])
                }

                if table_choice in table_map:
                    table_name, headers = table_map[table_choice]
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    
                    print(f"\n--- ALL RECORDS IN '{table_name.upper()}' ---")
                    if rows:
                        # Calculate maximum width for each column
                        column_widths = [len(header) for header in headers]
                        for row in rows:
                            for i, value in enumerate(row):
                                # Convert all values to string for length calculation
                                column_widths[i] = max(column_widths[i], len(str(value)))
                        
                        # Print headers
                        header_line = " | ".join(headers[i].ljust(column_widths[i]) for i in range(len(headers)))
                        print(header_line)
                        print("-" * len(header_line)) # Separator line based on total header length

                        # Print data rows
                        for row in rows:
                            # Format each value to its calculated width
                            formatted_row = []
                            for i, value in enumerate(row):
                                if isinstance(value, float):
                                    # Format floats for consistent display
                                    formatted_value = f"{value:.2f}"
                                else:
                                    formatted_value = str(value)
                                formatted_row.append(formatted_value.ljust(column_widths[i]))
                            print(" | ".join(formatted_row))
                    else:
                        print(f"No records found in the '{table_name}' table.")
                elif table_choice == 'b':
                    continue # Go back to display_data_menu
                else:
                    print("\n--- INVALID TABLE CHOICE ---")
                    print("Please select a valid table option (1-6 or 'b').")
                
            elif choice == '2':
                print("\n--- SEARCH BOOKS BY TITLE ---")
                keyword = input("Enter a keyword from the book title to search: ").strip()
                cursor.execute("SELECT isbn, book_title, category, rental_price, status, author, publisher FROM books WHERE book_title LIKE %s", ('%' + keyword + '%',))
                rows = cursor.fetchall()

                if rows:
                    print(f"\n--- SEARCH RESULTS for '{keyword}' ---")
                    for i, row in enumerate(rows):
                        print(f"\nBook {i+1}:")
                        print(f"  **ISBN**: {row[0]}")
                        print(f"  **Title**: {row[1]}")
                        print(f"  **Category**: {row[2]}")
                        print(f"  **Rental Price**: ${row[3]:.2f}")
                        print(f"  **Status**: {'Available' if row[4] == 'yes' else 'Issued'}")
                        print(f"  **Author**: {row[5]}")
                        print(f"  **Publisher**: {row[6]}")
                else:
                    print(f"\n--- NO RESULTS ---")
                    print(f"No books found with '{keyword}' in their title.")

            elif choice == 'b':
                break
            else:
                print("\n--- INVALID CHOICE ---")
                print("Please select a valid option (1, 2, or 'b').")
            input("\nPress Enter to continue...")

    except mysql.connector.Error as err:
        print(f"\n--- DATABASE ERROR ---")
        print(f"An error occurred during the operation: {err}")
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"Something went wrong: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def run_task(task_num):
    """Executes predefined database tasks and reports."""
    conn = None
    cursor = None
    try:
        conn = connect()
        if conn is None:
            return
        cursor = conn.cursor()

        print_banner() # Print banner before showing task output
        print(f"--- EXECUTING TASK {task_num} ---")

        task_description = {
            '1': "Adding a new book (**To Kill a Mockingbird**) for demonstration...",
            '2': "Updating member address for **'C101'**...",
            '3': "Deleting issued status record **'IS121'**...",
            '4': "Listing all books issued by employee **'E101'**...",
            '5': "Identifying members who have issued **more than one book**...",
            '6': "Creating/updating a summary table **'book_cnts'** showing issue counts...",
            '7': "Retrieving all books categorized as **'Classic'**...",
            '8': "Calculating total rental income and book count by category...",
            '9': "Finding members who registered in the **last 180 days**...",
            '10': "Listing employees along with their **branch manager's information**...",
            '11': "Creating a new table for books with a rental price **greater than $7**...",
            '12': "Listing books that have been issued but **not yet returned**...",
            '13': "Identifying members with **overdue books** (issued over 30 days ago and not returned)...",
            '14': "Updating the status of returned books to **'Available'** (Mass Update)...",
            '15': "Generating a comprehensive **branch performance report**...",
            '16': "Creating a table of **'active members'** (issued a book in last 2 months)...",
            '17': "Discovering **Top 3 Employees** by Books Processed..."
        }
        print(task_description.get(task_num, "Executing selected task..."))
        print("-" * 90) # Adjusted width for the new, wider banner

        if task_num == '1':
            cursor.execute("""
                INSERT INTO books(isbn, book_title, category, rental_price, status, author, publisher)
                VALUES ('978-1-60129-456-2', 'To Kill a Mockingbird', 'Classic', 6.00, 'yes', 'Harper Lee', 'J.B. Lippincott & Co.')
            """)
            conn.commit()
            print("\n**Book 'To Kill a Mockingbird' added.** Displaying the book records:")
            cursor.execute("SELECT isbn, book_title, category, rental_price, status, author FROM books WHERE isbn = '978-1-60129-456-2'")
        elif task_num == '2':
            cursor.execute("UPDATE members SET member_address = '125 Main St' WHERE member_id = 'C101'")
            conn.commit()
            print("\n**Address for Member 'C101' updated.** Displaying updated member details:")
            cursor.execute("SELECT member_id, member_name, member_address FROM members WHERE member_id = 'C101'")
        elif task_num == '3':
            # This task attempts to delete a record. To show the effect, we should try to add it first
            # if it doesn't exist to make sure the delete has something to act on for demo purposes.
            # However, for a simple demo, we'll assume it might exist or not.
            cursor.execute("DELETE FROM issued_status WHERE issued_id = 'IS121'")
            conn.commit()
            print("\n**Issued record 'IS121' deleted.** Displaying remaining issued status records (if any):")
            cursor.execute("SELECT issued_id, issued_member_id, issued_book_isbn FROM issued_status")
        elif task_num == '4':
            print("\n**Books issued by Employee 'E101':**")
            cursor.execute("SELECT issued_id, issued_book_isbn, issued_date FROM issued_status WHERE issued_emp_id = 'E101'")
        elif task_num == '5':
            print("\n**Members who have issued more than one book:**")
            cursor.execute("""
                SELECT m.member_name, COUNT(ist.issued_id) as books_issued_count
                FROM issued_status ist
                JOIN members m ON m.member_id = ist.issued_member_id
                GROUP BY m.member_name
                HAVING COUNT(ist.issued_id) > 1
                ORDER BY books_issued_count DESC
            """)
        elif task_num == '6':
            cursor.execute("DROP TABLE IF EXISTS book_cnts")
            cursor.execute("""
                CREATE TABLE book_cnts AS
                SELECT b.isbn, b.book_title, COUNT(ist.issued_id) as no_issued
                FROM books b
                JOIN issued_status ist ON ist.issued_book_isbn = b.isbn
                GROUP BY b.isbn, b.book_title
            """)
            conn.commit()
            print("\n**Summary table 'book_cnts' created.** Displaying its content:")
            cursor.execute("SELECT * FROM book_cnts")
        elif task_num == '7':
            print("\n**Books in 'Classic' category:**")
            cursor.execute("SELECT book_title, author, publisher, rental_price FROM books WHERE category = 'Classic'")
        elif task_num == '8':
            print("\n**Total rental income and count of issued books per category:**")
            cursor.execute("""
                SELECT b.category, SUM(b.rental_price) as total_rental_income, COUNT(ist.issued_id) as books_issued_count
                FROM books b
                JOIN issued_status ist ON ist.issued_book_isbn = b.isbn
                GROUP BY b.category
                ORDER BY total_rental_income DESC
            """)
        elif task_num == '9':
            print("\n**Members registered in the last 180 days:**")
            cursor.execute("SELECT member_name, member_address, reg_date FROM members WHERE reg_date >= CURDATE() - INTERVAL 180 DAY")
        elif task_num == '10':
            print("\n**Employees with their branch and manager details:**")
            # Note: The original branch table does not have 'branch_name'. Assuming a logical connection or a typo.
            # For this query to work accurately, 'branch' table would need a 'branch_name' column or 'branch_address' should be used.
            # I'll use branch_address for branch identification.
            # Also, 'emp_position' doesn't exist in the provided schema for employees, assuming 'position' field.
            cursor.execute("""
                SELECT e1.emp_name, e1.position, b.branch_address, e2.emp_name as manager_name
                FROM employees e1
                JOIN branch b ON b.branch_id = e1.branch_id
                LEFT JOIN employees e2 ON b.manager_id = e2.emp_id
                ORDER BY b.branch_address, e1.emp_name
            """)
        elif task_num == '11':
            cursor.execute("DROP TABLE IF EXISTS books_price_greater_than_seven")
            cursor.execute("""
                CREATE TABLE books_price_greater_than_seven AS
                SELECT isbn, book_title, rental_price, author FROM books WHERE rental_price > 7
            """)
            conn.commit()
            print("\n**Table 'books_price_greater_than_seven' created.** Displaying its content:")
            cursor.execute("SELECT * FROM books_price_greater_than_seven")
        elif task_num == '12':
            print("\n**Books currently issued and not yet returned:**")
            cursor.execute("""
                SELECT b.book_title, b.author, ist.issued_date, m.member_name
                FROM issued_status ist
                JOIN books b ON b.isbn = ist.issued_book_isbn
                JOIN members m ON m.member_id = ist.issued_member_id
                LEFT JOIN return_status rs ON ist.issued_id = rs.issued_id
                WHERE rs.return_id IS NULL
                ORDER BY ist.issued_date
            """)
        elif task_num == '13':
            print("\n**Members with overdue books (issued > 30 days and not returned):**")
            cursor.execute("""
                SELECT m.member_name, bk.book_title, ist.issued_date,
                        DATEDIFF(CURDATE(), ist.issued_date) as overdue_days
                FROM issued_status ist
                JOIN members m ON m.member_id = ist.issued_member_id
                JOIN books bk ON bk.isbn = ist.issued_book_isbn
                LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
                WHERE rs.return_id IS NULL AND DATEDIFF(CURDATE(), ist.issued_date) > 30
                ORDER BY overdue_days DESC
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
            print("\n**Book statuses updated for returned books.** Displaying a sample of updated book statuses:")
            cursor.execute("SELECT book_title, status FROM books WHERE status = 'yes' LIMIT 5")
        elif task_num == '15':
            cursor.execute("DROP TABLE IF EXISTS branch_reports")
            cursor.execute("""
                CREATE TABLE branch_reports AS
                SELECT b.branch_address as branch_name, -- Using branch_address as branch_name for report
                        COUNT(DISTINCT ist.issued_id) as books_issued,
                        COUNT(DISTINCT rs.return_id) as books_returned,
                        COALESCE(SUM(bk.rental_price), 0) as total_revenue
                FROM branch b
                LEFT JOIN employees e ON e.branch_id = b.branch_id
                LEFT JOIN issued_status ist ON ist.issued_emp_id = e.emp_id
                LEFT JOIN return_status rs ON rs.issued_id = ist.issued_id
                LEFT JOIN books bk ON ist.issued_book_isbn = bk.isbn
                GROUP BY b.branch_address
                ORDER BY total_revenue DESC
            """)
            conn.commit()
            print("\n**Branch performance report generated.** Displaying report:")
            cursor.execute("SELECT * FROM branch_reports")
        elif task_num == '16':
            cursor.execute("DROP TABLE IF EXISTS active_members")
            # The 'members' table does not have 'phone_no'. Removing it from the CREATE TABLE statement.
            cursor.execute("""
                CREATE TABLE active_members AS
                SELECT member_id, member_name, member_address, reg_date FROM members
                WHERE member_id IN (
                    SELECT DISTINCT issued_member_id
                    FROM issued_status
                    WHERE issued_date >= CURDATE() - INTERVAL 2 MONTH
                )
            """)
            conn.commit()
            print("\n**Table 'active_members' created.** Displaying active members:")
            cursor.execute("SELECT * FROM active_members")
        elif task_num == '17':
            print("\n**Top 3 Employees by Books Processed:**")
            cursor.execute("""
                SELECT e.emp_name, b.branch_address as branch_name, COUNT(ist.issued_id) as total_books_issued
                FROM issued_status ist
                JOIN employees e ON e.emp_id = ist.issued_emp_id
                JOIN branch b ON e.branch_id = b.branch_id
                GROUP BY e.emp_name, b.branch_address
                ORDER BY total_books_issued DESC LIMIT 3
            """)
        else:
            print("\n--- INVALID TASK NUMBER ---")
            print("Please enter a valid task number (1-17).")
            return

        rows = cursor.fetchall()
        if rows:
            print("\n--- RESULTS ---")
            # Attempt to print headers if available from cursor.description
            if cursor.description:
                headers = [i[0] for i in cursor.description]
                # Calculate max width for each column dynamically
                column_widths = [len(header) for header in headers]
                for row in rows:
                    for i, value in enumerate(row):
                        # Convert all values to string for length calculation
                        # Format floats to 2 decimal places if present
                        if isinstance(value, float):
                            str_value = f"{value:.2f}"
                        elif isinstance(value, (bytes, bytearray)):
                             str_value = value.decode('utf-8') # Decode bytes to string
                        else:
                            str_value = str(value)
                        column_widths[i] = max(column_widths[i], len(str_value))

                # Print headers
                header_line = " | ".join(headers[i].ljust(column_widths[i]) for i in range(len(headers)))
                print(header_line)
                print("-" * len(header_line))

                # Print data rows
                for row in rows:
                    formatted_row_data = []
                    for i, value in enumerate(row):
                        if isinstance(value, float):
                            formatted_value = f"{value:.2f}"
                        elif isinstance(value, (bytes, bytearray)):
                            formatted_value = value.decode('utf-8')
                        else:
                            formatted_value = str(value)
                        formatted_row_data.append(formatted_value.ljust(column_widths[i]))
                    print(" | ".join(formatted_row_data))
        else:
            print("\n--- NO DATA ---")
            print("No results found for this task, or the operation completed without returning data.")

    except mysql.connector.Error as err:
        print(f"\n--- DATABASE ERROR ---")
        print(f"An error occurred during task execution: {err}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"Something went wrong: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    input("\nPress Enter to return to Predefined Tasks menu...")

def predefined_tasks_menu():
    """Displays menu for predefined tasks and handles user choices."""
    while True:
        print_banner() # Print banner before showing the menu
        print("--- PREDEFINED TASKS & REPORTS ---")
        print(" These tasks perform specific database operations or generate reports.")
        print("\n **REPORTS & QUERIES:**")
        print("  1: Add a Sample Book (Demonstration)")
        print("  2: Update a Member's Address (Demonstration)")
        print("  3: Delete an Issued Record (Demonstration)")
        print("  4: List Books Issued by a Specific Employee")
        print("  5: Find Members Who Issued Multiple Books")
        print("  6: Create Summary Table of Book Issue Counts")
        print("  7: Retrieve All 'Classic' Books")
        print("  8: Calculate Total Rental Income & Issued Count by Category")
        print("  9: Show Members Registered in the Last 180 Days")
        print(" 10: View Employees with Their Branch Managers")
        print(" 11: Create Table for Books Priced Over $7")
        print(" 12: List Books Not Yet Returned")
        print(" 13: Identify Members with Overdue Books (>30 days)")
        print(" 14: Update Book Status After Return (Mass Update)")
        print(" 15: Generate Branch Performance Report")
        print(" 16: Create Table of Active Members (Issued in last 2 months)")
        print(" 17: Discover Top 3 Employees by Books Processed")
        print("\nb: Back to Main Menu")
        choice = input("\nEnter your task number: ").strip().lower()
        if choice == 'b':
            break
        elif choice.isdigit() and 1 <= int(choice) <= 17:
            run_task(choice)
        else:
            print("\n--- INVALID CHOICE ---")
            print("Please enter a valid task number (1-17) or 'b' to go back.")
            input("Press Enter to continue...")

def main():
    """Main function to run the Library CLI application."""
    while True:
        print_banner() # Print banner before showing the main menu
        print("--- MAIN MENU ---")
        print("Welcome to the Library Management System!")
        print("\n1. Add New Data")
        print("2. Remove Data")
        print("3. Display Data")
        print("4. Predefined Tasks / Reports")
        print("q. Quit the Application")
        choice = input("\nSelect an option: ").strip().lower()
        if choice == '1':
            add_new_data_menu()
        elif choice == '2':
            remove_data_menu()
        elif choice == '3':
            display_data_menu()
        elif choice == '4':
            predefined_tasks_menu()
        elif choice == 'q':
            print_banner() # Clear screen one last time
            print("\n" + "="*90) # Adjusted width for the new, wider banner
            print(f"{'Thank you for using the Library Management System!':^90}")
            print(f"{'Have a great day!':^99}") # Adjusted for better centering on longer line
            print("="*90 + "\n")
            time.sleep(1.5) # Small delay before exiting
            break
        else:
            print("\n--- INVALID CHOICE ---")
            print("Please select a valid option (1, 2, 3, 4, or 'q').")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()