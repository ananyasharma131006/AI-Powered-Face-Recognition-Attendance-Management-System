from datetime import datetime
import threading
from tkinter import messagebox
from gui.reports_window import open_reports_window
import customtkinter as ctk

from gui.register_window import open_register_window
from gui.students_window import open_students_window

from utils.database_manager import (
    get_total_students,
    get_today_attendance
)



# ----------------------------------------
# Attendance Thread Protection
# ----------------------------------------

attendance_running = False


def open_attendance():

    global attendance_running

    if attendance_running:

        messagebox.showinfo(
            "Attendance",
            "Attendance system is already running."
        )

        return

    attendance_running = True

    def run():

        global attendance_running

        try:

            from app import start_attendance

            start_attendance()

        finally:

            attendance_running = False

    threading.Thread(
        target=run,
        daemon=True
    ).start()


# ----------------------------------------
# Export Attendance
# ----------------------------------------

def export_attendance():

    success, result = export_attendance()

    if success:

        messagebox.showinfo(
            "Export Successful",
            f"Attendance exported successfully!\n\n{result}"
        )

    else:

        messagebox.showwarning(
            "Export Failed",
            result
        )


# ----------------------------------------
# Dashboard
# ----------------------------------------

def start_dashboard():

    students = get_total_students()
    attendance = get_today_attendance()

    # -----------------------------
    # Main Window
    # -----------------------------

    app = ctk.CTk()

    app.title("AI Face Recognition Attendance System")

    app.geometry("900x650")

    app.resizable(False, False)

    # -----------------------------
    # Header
    # -----------------------------

    header = ctk.CTkFrame(
        app,
        corner_radius=15,
        height=100
    )

    header.pack(
        fill="x",
        padx=20,
        pady=20
    )

    header.pack_propagate(False)

    title = ctk.CTkLabel(
        header,
        text="🎓 AI Face Recognition Attendance System",
        font=("Arial", 28, "bold")
    )

    title.pack(
        side="left",
        padx=20
    )

    clock_label = ctk.CTkLabel(
        header,
        text="",
        font=("Arial", 16)
    )

    clock_label.pack(
        side="right",
        padx=20
    )

    # -----------------------------
    # Live Clock
    # -----------------------------

    def update_clock():

        now = datetime.now()

        clock_label.configure(
            text=now.strftime(
                "%A\n%d %B %Y\n%I:%M:%S %p"
            )
        )

        app.after(1000, update_clock)

    update_clock()

    # -----------------------------
    # Statistics Cards
    # -----------------------------

    cards_frame = ctk.CTkFrame(
        app,
        fg_color="transparent"
    )

    cards_frame.pack(
        pady=10
    )

    # Student Card

    student_card = ctk.CTkFrame(
        cards_frame,
        width=300,
        height=130,
        corner_radius=15
    )

    student_card.pack(
        side="left",
        padx=15
    )

    student_card.pack_propagate(False)

    ctk.CTkLabel(
        student_card,
        text="👨‍🎓 Registered Students",
        font=("Arial", 20, "bold")
    ).pack(pady=(20, 5))

    students_label = ctk.CTkLabel(
        student_card,
        text=str(students),
        font=("Arial", 36, "bold")
    )

    students_label.pack()

    # Attendance Card

    attendance_card = ctk.CTkFrame(
        cards_frame,
        width=300,
        height=130,
        corner_radius=15
    )

    attendance_card.pack(
        side="left",
        padx=15
    )

    attendance_card.pack_propagate(False)

    ctk.CTkLabel(
        attendance_card,
        text="✅ Today's Attendance",
        font=("Arial", 20, "bold")
    ).pack(pady=(20, 5))

    attendance_label = ctk.CTkLabel(
        attendance_card,
        text=str(attendance),
        font=("Arial", 36, "bold")
    )

    attendance_label.pack()

    # -----------------------------
    # Auto Refresh
    # -----------------------------

    def refresh_dashboard():

        students_label.configure(
            text=str(get_total_students())
        )

        attendance_label.configure(
            text=str(get_today_attendance())
        )

        app.after(
            3000,
            refresh_dashboard
        )

    refresh_dashboard()

    # -----------------------------
    # Buttons
    # -----------------------------

    button_frame = ctk.CTkFrame(
        app
    )

    button_frame.pack(
        pady=35
    )

    register_btn = ctk.CTkButton(
        button_frame,
        text="👤 Register Student",
        width=250,
        height=70,
        command=open_register_window
    )

    register_btn.grid(
        row=0,
        column=0,
        padx=20,
        pady=20
    )

    attendance_btn = ctk.CTkButton(
        button_frame,
        text="🎥 Start Attendance",
        width=250,
        height=70,
        command=open_attendance
    )

    attendance_btn.grid(
        row=0,
        column=1,
        padx=20,
        pady=20
    )

    students_btn = ctk.CTkButton(
        button_frame,
        text="👥 View Students",
        width=250,
        height=70,
        command=open_students_window
    )

    students_btn.grid(
        row=1,
        column=0,
        padx=20,
        pady=20
    )

    export_btn = ctk.CTkButton(
    button_frame,
    text="📊 Reports",
    width=220,
    height=60,
    command=open_reports_window
    )
    export_btn.grid(
        row=1,
        column=1,
        padx=20,
        pady=20
    )

    # -----------------------------
    # Exit Button
    # -----------------------------

    exit_btn = ctk.CTkButton(
        app,
        text="❌ Exit",
        width=250,
        height=55,
        fg_color="red",
        hover_color="darkred",
        command=app.destroy
    )

    exit_btn.pack(
        pady=15
    )

    # -----------------------------
    # Status Bar
    # -----------------------------

    status_bar = ctk.CTkLabel(
        app,
        text="🟢 System Ready",
        font=("Arial", 14)
    )

    status_bar.pack(
        side="bottom",
        pady=10
    )

    app.mainloop()


if __name__ == "__main__":

    start_dashboard()