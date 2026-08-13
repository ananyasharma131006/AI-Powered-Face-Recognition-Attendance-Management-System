from tkinter import ttk,messagebox
from gui.edit_student_window import open_edit_window
import customtkinter as ctk
from utils.database_manager import (
    get_all_students,
    search_students,
    delete_student
)

from utils.file_manager import delete_student_files

def open_students_window():

    window = ctk.CTkToplevel()

    window.title("Registered Students")

    window.geometry("800x500")

    window.resizable(False, False)

    # ----------------------------
    # Title
    # ----------------------------

    ctk.CTkLabel(
        window,
        text="👥 Registered Students",
        font=("Arial", 24, "bold")
    ).pack(pady=(20, 10))

    # ----------------------------
    # Search Bar
    # ----------------------------

    search_var = ctk.StringVar()

    search_entry = ctk.CTkEntry(
        window,
        width=300,
        textvariable=search_var,
        placeholder_text="🔍 Search by Name or Roll Number"
    )

    search_entry.pack(pady=10)

    # ----------------------------
    # Treeview
    # ----------------------------

    tree = ttk.Treeview(
        window,
        columns=("ID", "Name", "Roll"),
        show="headings",
        height=12
    )

    tree.heading("ID", text="ID")
    tree.heading("Name", text="Student Name")
    tree.heading("Roll", text="Roll Number")

    tree.column("ID", width=70, anchor="center")
    tree.column("Name", width=350, anchor="center")
    tree.column("Roll", width=180, anchor="center")

    tree.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    # ----------------------------
    # Load Students
    # ----------------------------

    def load_students(data):

        tree.delete(*tree.get_children())

        for student in data:

            tree.insert(
                "",
                "end",
                values=student
            )

    load_students(get_all_students())

    # ----------------------------
    # Live Search
    # ----------------------------

    def perform_search(*args):

        keyword = search_var.get().strip()

        if keyword == "":

            load_students(get_all_students())

        else:

            load_students(
                search_students(keyword)
            )

    search_var.trace_add(
        "write",
        perform_search
    )
    def delete_selected_student():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
    
            "No Selection",
            "Please select a student.",
            parent=window
        )
            return

        values = tree.item(selected[0])["values"]

        student_id = values[0]
        student_name = values[1]
        roll_number = values[2]

        answer = messagebox.askyesno(
    
        "Delete Student",
        f"Delete {student_name} (Roll {roll_number})?",
        parent=window
    )

        if not answer:
            return

        student = delete_student(student_id)

        if student:

            delete_student_files(
            student[0],
            student[1]
        )

        load_students(get_all_students())

        messagebox.showinfo(
           
        "Success",
        "Student deleted successfully.",
        parent=window
    )
    def edit_selected_student():

        selected = tree.selection()

        if not selected:

            messagebox.showwarning(
                
            "No Selection",
            "Please select a student.",
            parent=window
        )
            return

        values = tree.item(selected[0])["values"]

        student_id = values[0]
        student_name = values[1]
        roll_number = values[2]

        open_edit_window(
        window,
        student_id,
        student_name,
        roll_number,
        lambda: load_students(get_all_students())
    )
    # ----------------------------
    # Bottom Buttons
    # ----------------------------

    button_frame = ctk.CTkFrame(
        window,
        fg_color="transparent"
    )

    button_frame.pack(pady=10)

    refresh_btn = ctk.CTkButton(
        button_frame,
        text="🔄 Refresh",
        width=150,
        command=lambda: load_students(get_all_students())
    )

    refresh_btn.grid(
        row=0,
        column=0,
        padx=10
    )
    edit_btn = ctk.CTkButton(
    button_frame,
    text="✏ Edit Student",
    width=150,
    command=edit_selected_student
)

    edit_btn.grid(
    row=0,
    column=1,
    padx=10
)
    delete_btn = ctk.CTkButton(
    button_frame,
    text="🗑 Delete Student",
    width=150,
    fg_color="red",
    hover_color="darkred",
    command=delete_selected_student
)

    delete_btn.grid(
    row=0,
    column=2,
    padx=10
)
    close_btn = ctk.CTkButton(
    button_frame,
    text="❌ Close",
    width=150,
    fg_color="gray40",
    hover_color="gray25",
    command=window.destroy
)

    close_btn.grid(
        row=0,
        column=3,
        padx=10
    )