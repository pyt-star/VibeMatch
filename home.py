import customtkinter as ctk
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vibematch"
)
cur = db.cursor()


def build_home(parent, user):

    for widget in parent.winfo_children():
        widget.destroy()

    parent.grid_columnconfigure((0, 1, 2), weight=1)
    parent.grid_rowconfigure(3, weight=1)

    titlemsg = ctk.CTkLabel(parent, text=f"Good Evening, {user}", font=("Arial", 22, "bold"))
    titlemsg.grid(row=0, column=0, columnspan=3, padx=20, pady=(15, 15), sticky="w")

