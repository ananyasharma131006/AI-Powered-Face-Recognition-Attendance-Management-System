import tkinter as tk
from tkinter import messagebox


def register_student():
    messagebox.showinfo(
        "Register",
        "Register Student clicked."
    )


def start_attendance():
    messagebox.showinfo(
        "Attendance",
        "Start Attendance clicked."
    )


root = tk.Tk()

root.title("AI Face Recognition Attendance System")

root.geometry("600x450")

root.resizable(False, False)


title = tk.Label(
    root,
    text="AI Face Recognition Attendance System",
    font=("Arial", 18, "bold")
)

title.pack(pady=25)


register_btn = tk.Button(
    root,
    text="Register Student",
    width=25,
    height=2,
    command=register_student
)

register_btn.pack(pady=10)


attendance_btn = tk.Button(
    root,
    text="Start Attendance",
    width=25,
    height=2,
    command=start_attendance
)

attendance_btn.pack(pady=10)


exit_btn = tk.Button(
    root,
    text="Exit",
    width=25,
    height=2,
    command=root.destroy
)

exit_btn.pack(pady=30)


root.mainloop()