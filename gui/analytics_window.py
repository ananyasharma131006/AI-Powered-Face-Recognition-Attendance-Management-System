import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from utils.database_manager import get_statistics_by_date


def open_analytics_window(report_date):

    total, present, absent, percentage = get_statistics_by_date(report_date)

    window = ctk.CTkToplevel()

    window.title("Attendance Analytics")

    window.geometry("900x500")

    window.resizable(False, False)

    window.grab_set()
    window.focus_force()

    # ----------------------------
    # Title
    # ----------------------------

    ctk.CTkLabel(
        window,
        text=f"📊 Attendance Analytics\n{report_date}",
        font=("Arial", 24, "bold")
    ).pack(pady=15)

    # ----------------------------
    # Charts Frame
    # ----------------------------

    charts_frame = ctk.CTkFrame(window)

    charts_frame.pack(fill="both", expand=True, padx=15, pady=10)

    # ----------------------------
    # Pie Chart
    # ----------------------------

    fig1 = plt.Figure(figsize=(4, 4), dpi=100)

    ax1 = fig1.add_subplot(111)

    ax1.pie(
        [present, absent],
        labels=["Present", "Absent"],
        autopct="%1.1f%%",
        startangle=90
    )

    ax1.set_title("Attendance Distribution")

    canvas1 = FigureCanvasTkAgg(
        fig1,
        master=charts_frame
    )

    canvas1.draw()

    canvas1.get_tk_widget().pack(
        side="left",
        fill="both",
        expand=True,
        padx=10
    )

    # ----------------------------
    # Bar Chart
    # ----------------------------

    fig2 = plt.Figure(figsize=(4, 4), dpi=100)

    ax2 = fig2.add_subplot(111)

    ax2.bar(
        ["Present", "Absent"],
        [present, absent]
    )

    ax2.set_ylabel("Students")

    ax2.set_title("Attendance Count")

    canvas2 = FigureCanvasTkAgg(
        fig2,
        master=charts_frame
    )

    canvas2.draw()

    canvas2.get_tk_widget().pack(
        side="right",
        fill="both",
        expand=True,
        padx=10
    )

    # ----------------------------
    # Close Button
    # ----------------------------

    ctk.CTkButton(
        window,
        text="Close",
        width=180,
        command=window.destroy
    ).pack(pady=15)