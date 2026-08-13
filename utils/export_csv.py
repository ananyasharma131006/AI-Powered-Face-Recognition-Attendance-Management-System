from pathlib import Path
import csv


def export_attendance_csv(records, report_date):
    """
    Exports attendance records to a CSV file.
    """

    if len(records) == 0:
        return False, "No attendance records found."

    reports_folder = Path("reports")
    reports_folder.mkdir(exist_ok=True)

    filename = reports_folder / f"Attendance_{report_date}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file)

        writer.writerow([
            "Roll Number",
            "Student Name",
            "Attendance Time"
        ])

        writer.writerows(records)

    return True, filename