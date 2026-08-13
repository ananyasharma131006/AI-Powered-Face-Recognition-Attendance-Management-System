from gui.analytics_window import open_analytics_window
import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import date
from utils.export_excel import export_attendance
from utils.database_manager import (
    get_attendance_by_date,
    get_statistics_by_date
)
from utils.export_csv import export_attendance_csv

def open_reports_window():

    # ----------------------------------------
    # Window
    # ----------------------------------------

    window = ctk.CTkToplevel()

    window.title("Attendance Reports")

    window.geometry("950x650")

    window.resizable(False, False)

    window.lift()
    window.focus_force()
    window.grab_set()

    # ----------------------------------------
    # Title
    # ----------------------------------------

    title = ctk.CTkLabel(
        window,
        text="📊 Attendance Reports",
        font=("Arial", 28, "bold")
    )

    title.pack(pady=20)

    # ----------------------------------------
    # Date Selection
    # ----------------------------------------

    date_frame = ctk.CTkFrame(window)

    date_frame.pack(pady=10)

    ctk.CTkLabel(
        date_frame,
        text="📅 Select Date",
        font=("Arial", 16, "bold")
    ).pack(side="left", padx=10)

    today = date.today()

    date_entry = DateEntry(
        date_frame,
        width=15,
        date_pattern="yyyy-mm-dd"
    )

    date_entry.set_date(today)

    date_entry.pack(
        side="left",
        padx=10
    )

    # ----------------------------------------
    # Statistics Frame
    # ----------------------------------------

    stats_frame = ctk.CTkFrame(window)

    stats_frame.pack(
        fill="x",
        padx=20,
        pady=20
    )

    total_label = ctk.CTkLabel(
        stats_frame,
        text="👨‍🎓 Total : 0",
        font=("Arial", 16, "bold")
    )

    total_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=20
    )

    present_label = ctk.CTkLabel(
        stats_frame,
        text="✅ Present : 0",
        font=("Arial", 16, "bold")
    )

    present_label.grid(
        row=0,
        column=1,
        padx=20
    )

    absent_label = ctk.CTkLabel(
        stats_frame,
        text="❌ Absent : 0",
        font=("Arial", 16, "bold")
    )

    absent_label.grid(
        row=0,
        column=2,
        padx=20
    )

    percentage_label = ctk.CTkLabel(
        stats_frame,
        text="📈 Attendance : 0%",
        font=("Arial", 16, "bold")
    )

    percentage_label.grid(
        row=0,
        column=3,
        padx=20
    )

    # ----------------------------------------
    # Attendance Table
    # ----------------------------------------

    tree = ttk.Treeview(
        window,
        columns=("Roll", "Name", "Time"),
        show="headings",
        height=16
    )

    tree.heading("Roll", text="Roll Number")
    tree.heading("Name", text="Student Name")
    tree.heading("Time", text="Attendance Time")

    tree.column(
        "Roll",
        width=150,
        anchor="center"
    )

    tree.column(
        "Name",
        width=420,
        anchor="center"
    )

    tree.column(
        "Time",
        width=220,
        anchor="center"
    )

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=10
    )

    # ----------------------------------------
    # Load Report Function
    # ----------------------------------------

    def load_report(selected_date):

        # Clear old data
        tree.delete(*tree.get_children())

        total, present, absent, percentage = \
            get_statistics_by_date(selected_date)

        total_label.configure(
            text=f"👨‍🎓 Total : {total}"
        )

        present_label.configure(
            text=f"✅ Present : {present}"
        )

        absent_label.configure(
            text=f"❌ Absent : {absent}"
        )

        percentage_label.configure(
            text=f"📈 Attendance : {percentage}%"
        )

        records = get_attendance_by_date(selected_date)

        for record in records:

            tree.insert(
                "",
                "end",
                values=record
            )


    
    # ----------------------------------------
    # Load Button
    # ----------------------------------------

    load_button = ctk.CTkButton(
        date_frame,
        text="🔄 Load Report",
        command=lambda: load_report(
            date_entry.get_date().strftime("%Y-%m-%d")
        )
    )

    load_button.pack(
        side="left",
        padx=10
    )

    # ----------------------------------------
    # Bottom Buttons
    # ----------------------------------------

    button_frame = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )

    button_frame.pack(
        pady=15
    )
    from tkinter import messagebox
    def export_excel():

        selected_date = date_entry.get_date().strftime("%Y-%m-%d")

        records = get_attendance_by_date(selected_date)

        success, result = export_attendance(
        records,
        selected_date
    )

        if success:

            messagebox.showinfo(
            "Success",
            f"Excel exported successfully!\n\n{result}"
        )

        else:

            messagebox.showwarning(
            "No Data",
            result
        )


    export_excel_btn = ctk.CTkButton(
    button_frame,
    text="📄 Export Excel",
    width=170,
    command=export_excel
    )

    export_excel_btn.grid(
        row=0,
        column=0,
        padx=10
    )
    from tkinter import messagebox

    def export_csv():

        selected_date = date_entry.get_date().strftime("%Y-%m-%d")

        records = get_attendance_by_date(selected_date)

        success, result = export_attendance_csv(
        records,
        selected_date
    )

        if success:

            messagebox.showinfo(
            "Success",
            f"CSV exported successfully!\n\n{result}"
        )

        else:

            messagebox.showwarning(
            "No Data",
            result
        )
    export_csv_btn = ctk.CTkButton(
    button_frame,
    text="📄 Export CSV",
    width=170,
    command=export_csv
    )

    export_csv_btn.grid(
        row=0,
        column=1,
        padx=10
    )
    analytics_btn = ctk.CTkButton(
    button_frame,
    text="📊 Analytics",
    width=170,
    command=lambda: open_analytics_window(
        date_entry.get_date().strftime("%Y-%m-%d")
    )
    )

    analytics_btn.grid(
    row=0,
    column=2,
    padx=10
    )
    close_btn = ctk.CTkButton(
        button_frame,
        text="❌ Close",
        width=170,
        fg_color="red",
        hover_color="darkred",
        command=window.destroy
    )

    close_btn.grid(
        row=0,
        column=3,
        padx=10
    )

    # ----------------------------------------
    # Initial Report
    # ----------------------------------------

    load_report(
        today.strftime("%Y-%m-%d")
    )