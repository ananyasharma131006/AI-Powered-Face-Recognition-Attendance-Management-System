import customtkinter as ctk
from tkinter import messagebox

from utils.database_manager import (
    add_student,
    student_exists
)

from utils.register_student import start_registration
from utils.face_encoder import generate_student_encoding


def open_register_window():
    """
    Opens the Register Student window.
    """

    window = ctk.CTkToplevel()

    window.title("Register Student")
    window.geometry("450x300")
    window.resizable(False, False)

    # Make the window appear above the dashboard
    window.transient(window.master)
    window.grab_set()

    # ----------------------------
    # Title
    # ----------------------------

    title = ctk.CTkLabel(
        window,
        text="👤 Register New Student",
        font=("Arial", 22, "bold")
    )
    title.pack(pady=20)

    # ----------------------------
    # Student Name
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="Student Name"
    ).pack()

    name_entry = ctk.CTkEntry(
        window,
        width=250
    )
    name_entry.pack(pady=5)

    # ----------------------------
    # Roll Number
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="Roll Number"
    ).pack()

    roll_entry = ctk.CTkEntry(
        window,
        width=250
    )
    roll_entry.pack(pady=5)

    # ----------------------------
    # Register Function
    # ----------------------------

    def register():

        name = name_entry.get().strip()
        roll = roll_entry.get().strip()

        # Validation
        if not name or not roll:

            messagebox.showerror(
                "Error",
                "All fields are required.",
                parent=window
            )
            return
        print("Name:", name)
        print("Roll:", roll)
        print("Exists:", student_exists(roll))
        # Duplicate check
        if student_exists(roll):

            messagebox.showerror(
            "Duplicate Roll Number",
            "A student with this roll number already exists.",
            parent=window
        )
            return

        # Capture Images
        success = start_registration(name, roll)

        if not success:

            messagebox.showwarning(
                "Cancelled",
                "Registration cancelled.",
                parent=window
            )
            return

        # Generate Face Encoding
        generate_student_encoding(name, roll)

        # Save to Database
        add_student(name, roll)

        messagebox.showinfo(
            "Success",
            "Student registered successfully!",
            parent=window
        )

        window.destroy()

    # ----------------------------
    # Register Button
    # ----------------------------

    register_button = ctk.CTkButton(
        window,
        text="Register Student",
        width=180,
        height=40,
        command=register
    )

    register_button.pack(pady=25)