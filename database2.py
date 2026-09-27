from tkinter.ttk import *
from tkinter import *
import mysql.connector
from tkinter import messagebox

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="vibematch"
)

mycursor = mydb.cursor()

def Register():
    Id = e1.get()
    Name = e2.get()
    Sem = e3.get()
    City = e4.get()

    Insert = "INSERT INTO student(id,name,sem,city) VALUES(%s,%s,%s,%s)"

    if(Id != "" and Name != "" and Sem != "" and City != ""):
        Value = (Id, Name, Sem, City)
        print(Value)
        mycursor.execute(Insert, Value)
        mydb.commit()
        messagebox.showinfo("Information", "Record inserted")
        Clear()   # clear after insert
    else:
        if (Id == "" and Name == "" and Sem == "" and City == ""):
            messagebox.showwarning("Warning", "Fill all details")
        else:
            messagebox.showwarning("Warning", "Some fields left blank")

def Clear():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

root = Tk()
root.title("Student Data")
root.geometry("500x200")

Label(root, text="RollNo", width=20, height=2, bg="pink").grid(row=0, column=0)
Label(root, text="Name", width=20, height=2, bg="pink").grid(row=1, column=0)
Label(root, text="Sem", width=20, height=2, bg="pink").grid(row=2, column=0)
Label(root, text="City", width=20, height=2, bg="pink").grid(row=3, column=0)

e1 = Entry(root, width=30, borderwidth=8)
e1.grid(row=0, column=1)

e2 = Entry(root, width=30, borderwidth=8)
e2.grid(row=1, column=1)

e3 = Entry(root, width=30, borderwidth=8)
e3.grid(row=2, column=1)

e4 = Entry(root, width=30, borderwidth=8)
e4.grid(row=3, column=1)

Button(root, text="Register", width=10, height=2, command=Register).grid(row=7, column=0)
Button(root, text="Clear", width=10, height=2, command=Clear).grid(row=7, column=1)

root.mainloop()