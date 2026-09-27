from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import dashboard

# Window
root = Tk()
root.title("VibeMatch - Login")
root.geometry("400x350")

# Load original image
bg_image = Image.open("bg.png")

# Background label
bg_label = Label(root)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Resize background dynamically
def resize_bg(event):
    new_width = event.width
    new_height = event.height

    resized = bg_image.resize((new_width, new_height))
    bg = ImageTk.PhotoImage(resized)

    bg_label.config(image=bg)
    bg_label.image = bg

root.bind("<Configure>", resize_bg)

# UI
Label(root, text="VIBEMATCH", font=("Arial", 20, "bold"), bg="white").pack(pady=20)

Label(root, text="Username", bg="white").pack()
e1 = Entry(root, width=30)
e1.pack(pady=5)

Label(root, text="Password", bg="white").pack()
e2 = Entry(root, width=30, show="*")
e2.pack(pady=5)

# Login Function
def Login():
    username = e1.get()
    password = e2.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please fill all fields")
    else:
        messagebox.showinfo("Success", "Welcome " + username + "!")
        root.destroy()               # Close login window
        dashboard.open_dashboard()   # Open dashboard

# Register Function
def Register():
    messagebox.showinfo("Register", "Register page coming soon!")

# Buttons
Button(root, text="Login", width=15, command=Login).pack(pady=10)
Button(root, text="Register", width=15, command=Register).pack()

root.mainloop()