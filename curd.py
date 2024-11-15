import mysql.connector
from mysql.connector import Error
from abc import ABC, abstractmethod

# Secure the database connection with private key
class DatabaseConnection:
    __private_key = "YOUR_PRIVATE_KEY_HERE"  # Replace with your key for added security

    @staticmethod
    def connect():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pavan",
                database=" mangementdate1"
            )
            if connection.is_connected():
                print("Database connection successful")
                return connection
        except Error as e:
            print(f"Database connection error: {e}")
            return None

# Abstract Base Class
class ManagementData(ABC):
    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass

# Student Operations Class
class StudentManagement(ManagementData):
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def create(self, department, rollnumber, name, dateofbirth, joindate, address, phonenumber):
        query = """
        INSERT INTO studentadmission (department, rollnumber, name, dateofbirth, joindate, address, phonenumber)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, (department, rollnumber, name, dateofbirth, joindate, address, phonenumber))
            self.connection.commit()
            print("Student added successfully.")
        except Error as e:
            print(f"Error while adding student: {e}")

    def read(self, rollnumber=None):
        query = "SELECT * FROM studentadmission" if not rollnumber else "SELECT * FROM studentadmission WHERE rollnumber = %s"
        try:
            self.cursor.execute(query, (rollnumber,) if rollnumber else None)
            results = self.cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No records found.")
        except Error as e:
            print(f"Error while reading data: {e}")

    def update(self, rollnumber, field, new_value):
        query = f"UPDATE studentadmission SET {field} = %s WHERE rollnumber = %s"
        try:
            self.cursor.execute(query, (new_value, rollnumber))
            self.connection.commit()
            print(f"Updated {field} successfully.")
        except Error as e:
            print(f"Error while updating data: {e}")

    def delete(self, rollnumber):
        query = "DELETE FROM studentadmission WHERE rollnumber = %s"
        try:
            self.cursor.execute(query, (rollnumber,))
            self.connection.commit()
            print(f"Deleted student with rollnumber {rollnumber}.")
        except Error as e:
            print(f"Error while deleting student: {e}")

# Attendance Operations
class Attendance:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def mark_attendance(self, rollnumber, date):
        query = "INSERT INTO attendance (rollnumber, date) VALUES (%s, %s)"
        try:
            self.cursor.execute(query, (rollnumber, date))
            self.connection.commit()
            print(f"Attendance marked for rollnumber {rollnumber} on {date}.")
        except Error as e:
            print(f"Error while marking attendance: {e}")

    def view_attendance(self, rollnumber):
        query = "SELECT * FROM attendance WHERE rollnumber = %s"
        try:
            self.cursor.execute(query, (rollnumber,))
            results = self.cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No attendance records found.")
        except Error as e:
            print(f"Error while viewing attendance: {e}")

# Fee Payment Operations
class FeePayment:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def record_payment(self, rollnumber, amount):
        query = "INSERT INTO fee_payment (rollnumber, amount, payment_date) VALUES (%s, %s, NOW())"
        try:
            self.cursor.execute(query, (rollnumber, amount))
            self.connection.commit()
            print(f"Fee payment of {amount} recorded for rollnumber {rollnumber}.")
        except Error as e:
            print(f"Error while recording payment: {e}")

    def view_payments(self, rollnumber):
        query = "SELECT * FROM fee_payment WHERE rollnumber = %s"
        try:
            self.cursor.execute(query, (rollnumber,))
            results = self.cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No payment records found.")
        except Error as e:
            print(f"Error while viewing payments: {e}")

# Main Application
def main():
    db_connection = DatabaseConnection.connect()
    if not db_connection:
        print("Cannot proceed without database connection.")
        return
    cursor = db_connection.cursor()

    student_ops = StudentManagement(cursor, db_connection)
    attendance_ops = Attendance(cursor, db_connection)
    fee_ops = FeePayment(cursor, db_connection)

    print("Welcome to the College Management System!")

    while True:
        choice = input("""
        Choose an option:
        1. Add New Student
        2. View Student Data
        3. Update Student Data
        4. Delete Student Data
        5. Mark Attendance
        6. View Attendance
        7. Record Fee Payment
        8. View Fee Payments
        9. Exit
        Enter your choice: """)

        if choice == "1":
            department = input("Department: ")
            rollnumber = input("Roll Number: ")
            name = input("Name: ")
            dob = input("Date of Birth (YYYY-MM-DD): ")
            join_date = input("Join Date (YYYY-MM-DD): ")
            address = input("Address: ")
            phone = input("Phone Number: ")
            student_ops.create(department, rollnumber, name, dob, join_date, address, phone)
        elif choice == "2":
            rollnumber = input("Enter Roll Number (or press Enter to view all): ")
            student_ops.read(rollnumber or None)
        elif choice == "3":
            rollnumber = input("Roll Number to update: ")
            field = input("Field to update: ")
            new_value = input("New value: ")
            student_ops.update(rollnumber, field, new_value)
        elif choice == "4":
            rollnumber = input("Roll Number to delete: ")
            student_ops.delete(rollnumber)
        elif choice == "5":
            rollnumber = input("Roll Number: ")
            date = input("Date (YYYY-MM-DD): ")
            attendance_ops.mark_attendance(rollnumber, date)
        elif choice == "6":
            rollnumber = input("Roll Number: ")
            attendance_ops.view_attendance(rollnumber)
        elif choice == "7":
            rollnumber = input("Roll Number: ")
            amount = input("Amount: ")
            fee_ops.record_payment(rollnumber, amount)
        elif choice == "8":
            rollnumber = input("Roll Number: ")
            fee_ops.view_payments(rollnumber)
        elif choice == "9":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

if __name__ == "__main__":
    main()
