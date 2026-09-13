import mysql.connector
from datetime import datetime


def mark_attendance(student_id):

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shagun75",
        database="face_attendance"
    )

    cursor = connection.cursor()

    today = datetime.now().date()
    current_time = datetime.now().time()

    # Find student
    cursor.execute(
        "SELECT student_name FROM students WHERE student_id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        print(f"Student ID {student_id} not found.")

        cursor.close()
        connection.close()
        return

    student_name = student[0]

    # Check if attendance is already marked today
    cursor.execute(
        """SELECT attendance_id
           FROM attendance
           WHERE student_id = %s
           AND attendance_date = %s""",
        (student_id, today)
    )

    existing_attendance = cursor.fetchone()

    if existing_attendance is None:

        cursor.execute(
            """INSERT INTO attendance
               (student_id, attendance_date, attendance_time, status)
               VALUES (%s, %s, %s, %s)""",
            (student_id, today, current_time, "Present")
        )

        connection.commit()

        print(f"Attendance marked: {student_name}")

    else:
        print(f"{student_name} already marked today.")

    cursor.close()
    connection.close()