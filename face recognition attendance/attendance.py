import csv
import os
from datetime import datetime


def mark_attendance(student_id):
    filename = "attendance.csv"

    today = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # Check whether student is already marked today
    already_marked = False

    if os.path.exists(filename):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)

            for row in reader:
                if len(row) >= 2:
                    if row[0] == str(student_id) and row[1] == today:
                        already_marked = True
                        break

    # Mark attendance only once per day
    if not already_marked:
        with open(filename, "a", newline="") as file:
            writer = csv.writer(file)

            # Add header if file is empty/new
            if os.path.getsize(filename) == 0:
                writer.writerow(["Student ID", "Date", "Time", "Status"])

            writer.writerow([
                student_id,
                today,
                current_time,
                "Present"
            ])

        print(f"Attendance marked for Student {student_id}")
    else:
        print(f"Student {student_id} already marked today.")