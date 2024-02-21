import psycopg2
from psycopg2 import sql

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host="localhost", port="5432", database="test_4",
    user="postgres", password="808as808")
cursor = connection.cursor()

def list_all_students():
    cursor.execute("SELECT * FROM student ORDER BY sno")
    students = cursor.fetchall()
    if students:
        print("Listing all students:")
        for student in students:
            print(student)
    else:
        print("No students found.")

def check_student_exists(sno):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM student WHERE sno = %s)", (sno,))
    return cursor.fetchone()[0]

def insert_student(sno, sname, sage, sgender, sdept):
    if check_student_exists(sno):
        print("Student number already exists. Please re-enter.")
    else:
        cursor.execute("INSERT INTO student (sno, sname, sage, sgender, sdept) VALUES (%s, %s, %s, %s, %s)",
                       (sno, sname, sage, sgender, sdept))
        connection.commit()
        print("Student inserted successfully.")

def read_student(sno):
    cursor.execute("SELECT * FROM student WHERE sno = %s", (sno,))
    student = cursor.fetchone()
    if student:
        print("Student Information:", student)
    else:
        print("Student not found.")

def update_student(sno):
    read_student(sno)
    sname = input("Enter new name: ")
    sage = input("Enter new age: ")
    sgender = input("Enter new gender: ")
    sdept = input("Enter new department name: ")
    cursor.execute("UPDATE student SET sname = %s, sage = %s, sgender = %s, sdept = %s WHERE sno = %s",
                   (sname, sage, sgender, sdept, sno))
    connection.commit()
    print("Student updated successfully.")
    read_student(sno)

def delete_student(sno):
    if check_student_exists(sno):
        cursor.execute("DELETE FROM sc WHERE sno = %s", (sno,))
        cursor.execute("DELETE FROM student WHERE sno = %s", (sno,))
        connection.commit()
        print("Student and any enrollments deleted successfully.")
    else:
        print("Student not found.")


list_all_students()
# Example usage
# Read a student's information
read_student('20200001')

# Insert a new student
insert_student('20200005', 'Liang', 22, 'M', 'CS')
list_all_students()

# Update a student's information
update_student('20200005')
list_all_students()

# Delete a student's information
delete_student('20200005')
list_all_students()

# Don't forget to close the connection when done
cursor.close()
connection.close()
