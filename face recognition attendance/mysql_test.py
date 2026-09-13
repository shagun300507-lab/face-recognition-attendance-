import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="shagun75",
        database="face_attendance"
    )

    print("MySQL connected successfully!")

    connection.close()

except mysql.connector.Error as error:
    print("MySQL connection failed!")
    print(error)