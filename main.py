# Leo Keenan #
# 101222357  #

import psycopg2

# variables to get into PGAdmin #
dbname = 'Assignment3'
user = 'postgres'
password = '4366'
host = 'localhost'
port = '5432'

def getAllStudents():
    query = 'SELECT * FROM students'
    cursor.execute(query)

    rows = cursor.fetchall()
    for row in rows:
        student_id, first_name, last_name, email, enrollment_date = row
        print(f"({student_id}, '{first_name}', '{last_name}', '{email}', {enrollment_date.strftime('%Y-%m-%d')})")


def addStudent(first_name, last_name, email, enrollment_date):
    query = f"INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('{first_name}', '{last_name}', '{email}', '{enrollment_date}')"
    cursor.execute(query)
    conn.commit()

def updateStudentEmail(student_id, new_email):
    query = f"UPDATE students SET email = '{new_email}' WHERE student_id = {student_id}"
    cursor.execute(query)
    conn.commit()

def deleteStudent(student_id):
    query = f'DELETE FROM students WHERE student_id = {student_id}'
    cursor.execute(query)
    conn.commit()

def run():
    configure_table()
    while 1:
        print('Select one of the options below to interact with the database:\n'
              '1 - Retrieve and display all records from the students table\n'
              '2 - Insert a new student record into the students table\n'
              '3 - Update the email address for a student with the specified student_id\n'
              '4 - Delete the record of the student with the specified student_id\n'
              '5 - Exit\n')
        option = int(input())

        if option == 1:
            getAllStudents()
        elif option == 2:
            new_student = input('Enter the fields for the new student in the following space-separated format:\n'
                     'first_name last_name email enrollment_date\n')
            f_name, l_name, email, enrollment = new_student.split()
            addStudent(f_name, l_name, email, enrollment)
        elif option == 3:
            updated_student = input('Enter the student\'s ID and their updated email in the following space-separated format:\n'
                                    'student_id new_email\n')
            id, new_email = updated_student.split()
            updateStudentEmail(id, new_email)
        elif option == 4:
            student = input('Enter the ID of the student to delete:\n')
            deleteStudent(student)
        elif option == 5:
            break

        print('\n----------------------------------------------------------------------------\n')

# Reseting the Table, if you run the code, you will be starting from the same initial data everytime #
def configure_table():
    cursor.execute("DROP TABLE IF EXISTS students")
    cursor.execute("CREATE TABLE IF NOT EXISTS students (student_id SERIAL PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, enrollment_date DATE);")
    cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES ('John', 'Doe', 'john.doe@example.com', '2023-09-01'), ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'), ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');")
    conn.commit()

# Connecting to Database #
try:
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
except psycopg2.OperationalError as e:
    print(f'Error: {e}')
    exit(1)

# so I don't have to use conn.cursor every time #
cursor = conn.cursor()

run()

cursor.close()
conn.close()