import customtkinter as ctk
from tkinter import messagebox

from utils.database_manager import update_student
from utils.file_manager import rename_student_files


def open_edit_window(
    parent,
    student_id,
    old_name,
    old_roll,
    refresh_callback
):

    window = ctk.CTkToplevel(parent)

    window.title("Edit Student")

    window.geometry("450x320")

    window.resizable(False, False)

    window.grab_set()

    # ----------------------------
    # Title
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="✏ Edit Student Details",
        font=("Arial", 24, "bold")
    ).pack(pady=20)

    # ----------------------------
    # Name
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="Student Name",
        font=("Arial", 15)
    ).pack(anchor="w", padx=35)

    name_entry = ctk.CTkEntry(
        window,
        width=360
    )

    name_entry.insert(0, old_name)

    name_entry.pack(pady=(5, 15))

    # ----------------------------
    # Roll Number
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="Roll Number",
        font=("Arial", 15)
    ).pack(anchor="w", padx=35)

    roll_entry = ctk.CTkEntry(
        window,
        width=360
    )

    roll_entry.insert(0, old_roll)

    roll_entry.pack(pady=(5, 25))

    # ----------------------------
    # Save
    # ----------------------------

    def save_changes():

        new_name = name_entry.get().strip()
        new_roll = roll_entry.get().strip()

        if new_name == "" or new_roll == "":

            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        success = update_student(
            student_id,
            new_name,
            new_roll
        )

        if not success:

            messagebox.showerror(
                "Error",
                "Roll number already exists."
            )
            return

        rename_student_files(
            old_name,
            old_roll,
            new_name,
            new_roll
        )

        messagebox.showinfo(
            "Success",
            "Student updated successfully."
        )

        refresh_callback()

        window.destroy()

    # ----------------------------
    # Buttons
    # ----------------------------

    button_frame = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )

    button_frame.pack()

    save_btn = ctk.CTkButton(
        button_frame,
        text="💾 Save Changes",
        width=160,
        command=save_changes
    )

    save_btn.grid(
        row=0,
        column=0,
        padx=10
    )

    cancel_btn = ctk.CTkButton(
        button_frame,
        text="❌ Cancel",
        width=160,
        fg_color="red",
        hover_color="darkred",
        command=window.destroy
    )

    cancel_btn.grid(
        row=0,
        column=1,
        padx=10
    )