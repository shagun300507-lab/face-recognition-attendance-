import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import subprocess
import sys

# ==========================================
# START FACE RECOGNITION
# ==========================================

def start_recognition():
    try:
        subprocess.Popen(
            [sys.executable, "recognize.py"]
        )
    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not start face recognition:\n{error}"
        )
def view_statistics():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shagun75",
            database="face_attendance"
        )

        cursor = connection.cursor()

        # Total students
        cursor.execute(
            "SELECT COUNT(*) FROM students"
        )

        total_students = cursor.fetchone()[0]


        # Total attendance records
        cursor.execute(
            "SELECT COUNT(*) FROM attendance"
        )

        total_attendance = cursor.fetchone()[0]


        # Today's attendance
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM attendance
            WHERE attendance_date = CURDATE()
            """
        )

        today_attendance = cursor.fetchone()[0]


        # Attendance percentage
        if total_students > 0:

            percentage = (
                today_attendance / total_students
            ) * 100

        else:

            percentage = 0


        cursor.close()
        connection.close()


        # Statistics window
        stats_window = tk.Toplevel(root)

        stats_window.title("Attendance Statistics")
        stats_window.geometry("500x400")


        tk.Label(
            stats_window,
            text="Attendance Dashboard",
            font=("Arial", 20, "bold")
        ).pack(pady=25)


        tk.Label(
            stats_window,
            text=f"Total Students: {total_students}",
            font=("Arial", 14)
        ).pack(pady=10)


        tk.Label(
            stats_window,
            text=f"Total Attendance Records: {total_attendance}",
            font=("Arial", 14)
        ).pack(pady=10)


        tk.Label(
            stats_window,
            text=f"Today's Attendance: {today_attendance}",
            font=("Arial", 14)
        ).pack(pady=10)


        tk.Label(
            stats_window,
            text=f"Today's Attendance Percentage: {percentage:.1f}%",
            font=("Arial", 14, "bold")
        ).pack(pady=10)


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )

# ==========================================
# VIEW ATTENDANCE
# ==========================================

def view_attendance():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shagun75",
            database="face_attendance"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                a.attendance_id,
                s.student_id,
                s.student_name,
                a.attendance_date,
                a.attendance_time,
                a.status
            FROM attendance a
            JOIN students s
            ON a.student_id = s.student_id
            ORDER BY a.attendance_date DESC,
                     a.attendance_time DESC
        """)

        records = cursor.fetchall()

        cursor.close()
        connection.close()


        # Attendance window
        attendance_window = tk.Toplevel(root)
        attendance_window.title("Attendance Records")
        attendance_window.geometry("850x500")


        title = tk.Label(
            attendance_window,
            text="Attendance Records",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)


        columns = (
            "ID",
            "Student ID",
            "Name",
            "Date",
            "Time",
            "Status"
        )


        table = ttk.Treeview(
            attendance_window,
            columns=columns,
            show="headings"
        )


        table.heading("ID", text="ID")
        table.heading("Student ID", text="Student ID")
        table.heading("Name", text="Name")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")
        table.heading("Status", text="Status")


        table.column("ID", width=60)
        table.column("Student ID", width=100)
        table.column("Name", width=200)
        table.column("Date", width=120)
        table.column("Time", width=120)
        table.column("Status", width=100)


        for record in records:
            table.insert(
                "",
                tk.END,
                values=record
            )


        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )
def filter_attendance():

    filter_window = tk.Toplevel(root)
    filter_window.title("Attendance Filter")
    filter_window.geometry("850x550")

    tk.Label(
        filter_window,
        text="Attendance Filter",
        font=("Arial", 18, "bold")
    ).pack(pady=15)

    # Student ID
    tk.Label(
        filter_window,
        text="Student ID:",
        font=("Arial", 11)
    ).pack()

    student_entry = tk.Entry(
        filter_window,
        font=("Arial", 11)
    )
    student_entry.pack(pady=5)

    # Date
    tk.Label(
        filter_window,
        text="Date (YYYY-MM-DD):",
        font=("Arial", 11)
    ).pack()

    date_entry = tk.Entry(
        filter_window,
        font=("Arial", 11)
    )
    date_entry.pack(pady=5)

    def search_attendance():

        student_id = student_entry.get().strip()
        attendance_date = date_entry.get().strip()

        try:

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="shagun75",
                database="face_attendance"
            )

            cursor = connection.cursor()

            query = """
                SELECT
                    a.attendance_id,
                    s.student_id,
                    s.student_name,
                    a.attendance_date,
                    a.attendance_time,
                    a.status
                FROM attendance a
                JOIN students s
                ON a.student_id = s.student_id
                WHERE 1=1
            """

            values = []

            # Filter by Student ID
            if student_id:
                query += " AND s.student_id = %s"
                values.append(int(student_id))

            # Filter by Date
            if attendance_date:
                query += " AND a.attendance_date = %s"
                values.append(attendance_date)

            query += """
                ORDER BY a.attendance_date DESC,
                         a.attendance_time DESC
            """

            cursor.execute(query, values)

            records = cursor.fetchall()

            cursor.close()
            connection.close()

            # Clear old results
            for item in table.get_children():
                table.delete(item)

            # Display results
            for record in records:
                table.insert(
                    "",
                    tk.END,
                    values=record
                )

        except ValueError:

            messagebox.showwarning(
                "Input Error",
                "Student ID must be a number."
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def show_all():

        student_entry.delete(0, tk.END)
        date_entry.delete(0, tk.END)

        search_attendance()


    # Search button
    tk.Button(
        filter_window,
        text="Apply Filter",
        font=("Arial", 11),
        width=15,
        command=search_attendance
    ).pack(pady=10)


    # Show all button
    tk.Button(
        filter_window,
        text="Show All",
        font=("Arial", 11),
        width=15,
        command=show_all
    ).pack(pady=5)


    # Attendance table

    columns = (
        "ID",
        "Student ID",
        "Name",
        "Date",
        "Time",
        "Status"
    )

    table = ttk.Treeview(
        filter_window,
        columns=columns,
        show="headings"
    )

    table.heading("ID", text="ID")
    table.heading("Student ID", text="Student ID")
    table.heading("Name", text="Name")
    table.heading("Date", text="Date")
    table.heading("Time", text="Time")
    table.heading("Status", text="Status")

    table.column("ID", width=50)
    table.column("Student ID", width=100)
    table.column("Name", width=180)
    table.column("Date", width=120)
    table.column("Time", width=120)
    table.column("Status", width=100)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    # Show all records when window opens
    search_attendance()


# ==========================================
# VIEW REGISTERED STUDENTS
# ==========================================

def view_students():

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shagun75",
            database="face_attendance"
        )

        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, student_name
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()

        cursor.close()
        connection.close()


        # Student window
        student_window = tk.Toplevel(root)
        student_window.title("Registered Students")
        student_window.geometry("600x400")


        title = tk.Label(
            student_window,
            text="Registered Students",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=15)


        columns = (
            "Student ID",
            "Student Name"
        )


        table = ttk.Treeview(
            student_window,
            columns=columns,
            show="headings"
        )


        table.heading(
            "Student ID",
            text="Student ID"
        )

        table.heading(
            "Student Name",
            text="Student Name"
        )


        table.column(
            "Student ID",
            width=150
        )

        table.column(
            "Student Name",
            width=300
        )


        for student in students:

            table.insert(
                "",
                tk.END,
                values=student
            )


        table.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )


    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ==========================================
# REGISTER NEW STUDENT
# ==========================================

def add_student():

    add_window = tk.Toplevel(root)

    add_window.title("Register Student")

    add_window.geometry("450x300")


    # Student ID
    tk.Label(
        add_window,
        text="Student ID",
        font=("Arial", 12)
    ).pack(pady=10)


    id_entry = tk.Entry(
        add_window,
        font=("Arial", 12)
    )

    id_entry.pack()


    # Student Name
    tk.Label(
        add_window,
        text="Student Name",
        font=("Arial", 12)
    ).pack(pady=10)


    name_entry = tk.Entry(
        add_window,
        font=("Arial", 12)
    )

    name_entry.pack()


    # Save student
    def save_student():

        student_id = id_entry.get().strip()

        student_name = name_entry.get().strip()


        # Check empty fields
        if not student_id or not student_name:

            messagebox.showwarning(
                "Input Error",
                "Please enter Student ID and Student Name."
            )

            return


        # Check ID is number
        if not student_id.isdigit():

            messagebox.showwarning(
                "Input Error",
                "Student ID must be a number."
            )

            return


        try:

            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="shagun75",
                database="face_attendance"
            )


            cursor = connection.cursor()


            cursor.execute(
                """
                INSERT INTO students
                (student_id, student_name)
                VALUES (%s, %s)
                """,
                (
                    int(student_id),
                    student_name
                )
            )


            connection.commit()


            cursor.close()

            connection.close()


            messagebox.showinfo(
                "Success",
                "Student registered successfully!"
            )


            # Clear fields
            id_entry.delete(
                0,
                tk.END
            )

            name_entry.delete(
                0,
                tk.END
            )


        except mysql.connector.IntegrityError:

            messagebox.showerror(
                "Error",
                "Student ID already exists."
            )


        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )


    # Save button
    tk.Button(
        add_window,
        text="Save Student",
        font=("Arial", 12),
        width=20,
        command=save_student
    ).pack(pady=20)
# ==========================================
# CAPTURE STUDENT FACE
# ==========================================
def capture_face():

    capture_window = tk.Toplevel(root)

    capture_window.title("Capture Student Face")
    capture_window.geometry("450x250")


    tk.Label(
        capture_window,
        text="Enter Student ID",
        font=("Arial", 12)
    ).pack(pady=15)


    id_entry = tk.Entry(
        capture_window,
        font=("Arial", 12)
    )

    id_entry.pack()


    def start_capture():

        student_id = id_entry.get().strip()


        if not student_id:

            messagebox.showwarning(
                "Input Error",
                "Please enter Student ID."
            )

            return


        if not student_id.isdigit():

            messagebox.showwarning(
                "Input Error",
                "Student ID must be a number."
            )

            return


        try:

            # Start face capture
            capture_process = subprocess.Popen(
                [
                    sys.executable,
                    "capture_student_faces.py",
                    student_id
                ]
            )


            # Wait until face capture finishes
            def check_capture():

                if capture_process.poll() is None:

                    capture_window.after(
                        500,
                        check_capture
                    )

                else:

                    # Capture completed
                    # Now automatically train model

                    messagebox.showinfo(
                        "Face Capture",
                        "Face capture completed!\n\nStarting model training..."
                    )


                    subprocess.Popen(
                        [
                            sys.executable,
                            "train_model.py"
                        ]
                    )


                    capture_window.destroy()


            check_capture()


        except Exception as error:

            messagebox.showerror(
                "Error",
                f"Could not start face capture:\n{error}"
            )


    tk.Button(
        capture_window,
        text="Start Face Capture",
        font=("Arial", 12),
        width=20,
        command=start_capture
    ).pack(pady=25)

# ==========================================
# MAIN GUI WINDOW
# ==========================================

root = tk.Tk()

root.title("Face Recognition Attendance System")

root.geometry("500x550")


# Heading
title = tk.Label(
    root,
    text="Face Recognition Attendance System",
    font=("Arial", 18, "bold")
)

title.pack(pady=30)


# ==========================================
# START RECOGNITION BUTTON
# ==========================================

recognition_button = tk.Button(
    root,
    text="Start Face Recognition",
    font=("Arial", 12),
    width=30,
    command=start_recognition
)

recognition_button.pack(pady=15)


# ==========================================
# VIEW ATTENDANCE BUTTON
# ==========================================

attendance_button = tk.Button(
    root,
    text="View Attendance",
    font=("Arial", 12),
    width=30,
    command=view_attendance
)

attendance_button.pack(pady=15)


# ==========================================
# VIEW STUDENTS BUTTON
# ==========================================

students_button = tk.Button(
    root,
    text="View Students",
    font=("Arial", 12),
    width=30,
    command=view_students
)

students_button.pack(pady=15)


# ==========================================
# REGISTER STUDENT BUTTON
# ==========================================

register_button = tk.Button(
    root,
    text="Register Student",
    font=("Arial", 12),
    width=30,
    command=add_student
)

register_button.pack(pady=15)


# ==========================================
# EXIT BUTTON
# ==========================================
filter_button = tk.Button(
    root,
    text="Filter Attendance",
    font=("Arial", 12),
    width=30,
    command=filter_attendance
)

filter_button.pack(pady=15)


exit_button = tk.Button(
    root,
    text="Exit",
    font=("Arial", 12),
    width=30,
    command=root.destroy
)

exit_button.pack(pady=15)



# ==========================================
# RUN GUI
# ==========================================

root.mainloop()