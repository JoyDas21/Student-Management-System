import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql


sms = tk.Tk()
sms.geometry("1350x800+0+0")
sms.title("Student Management System")
sms.config(background="navyblue")

# Title....

title_label = tk.Label(sms, text="Student Management System", font=("Arial", 30, "bold"), border=12, relief=tk.GROOVE, background="navyblue", foreground="yellow")
title_label.pack(side=tk.TOP, fill=tk.X)

# Detail....

detail_frame = tk.LabelFrame(sms, border=10, relief=tk.GROOVE, background="navyblue", foreground="yellow")
detail_frame.place(x=30, y=180, width=420, height=450)

data_frame = tk.LabelFrame(sms, border=10, relief=tk.GROOVE, bg="navyblue")
data_frame.place(x=500, y=120, width=800, height=575)

# Variables....

name = tk.StringVar()
id_val = tk.StringVar()
section = tk.StringVar()
gender = tk.StringVar()

# Entry....

name_label = tk.Label(detail_frame, text="Name", background="navyblue", font=("Arial", 18), foreground="yellow")
name_label.grid(row=0, column=0, padx=8, pady=8, sticky=tk.W)

name_entry = tk.Entry(detail_frame, background="white", font=("Arial",18), textvariable=name)
name_entry.grid(row=0, column=1, padx=8, pady=8)

id_label = tk.Label(detail_frame, text="ID", background="navyblue", font=("Arial", 18), foreground="yellow")
id_label.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)

id_entry = tk.Entry(detail_frame, background="white", font=("Arial",18), textvariable=id_val)
id_entry.grid(row=1, column=1, padx=8, pady=8)

section_label = tk.Label(detail_frame, text="Section", background="navyblue", font=("Arial", 18), foreground="yellow")
section_label.grid(row=2, column=0, padx=8, pady=8, sticky=tk.W)

section_entry = tk.Entry(detail_frame, background="white", font=("Arial",18), textvariable=section)
section_entry.grid(row=2, column=1, padx=8, pady=8)

gender_label = tk.Label(detail_frame, text="Gender", background="navyblue", font=("Arial", 18), foreground="yellow")
gender_label.grid(row=3, column=0, padx=8, pady=8, sticky=tk.W)

gender_entry = ttk.Combobox(detail_frame, font=("Arial", 18), background="white", state="readonly", textvariable=gender)
gender_entry['values'] = ("Male", "Female", "Others")
gender_entry.grid(row=3, column=1, padx=8, pady=8)

# Functions....

def connect_data():
    conn = pymysql.connect(host="localhost", user="root", password="", database="student management system")
    curr = conn.cursor()
    curr.execute("Select * from data")
    rows = curr.fetchall()
    if len(rows) != 0:
        monitor.delete(*monitor.get_children())
        for row in rows:
            monitor.insert('', tk.END, values=row)
        conn.commit()
    conn.close()

def add_function():
    if name.get() == " " or id_entry.get() == " " or section.get() == " " or gender.get() == " ":
        messagebox.showerror("Error!", "Please Fill All Inputs!")
    else:
        conn = pymysql.connect(host="localhost", user="root", password="", database="student management system")
        curr = conn.cursor()
        curr.execute("Insert into data values(%s,%s,%s,%s)", (name.get(), id_val.get(), section.get(), gender.get()))
        conn.commit()
        conn.close()
        connect_data()

def fetch_data(event):

    cursor_row = monitor.focus()
    content = monitor.item(cursor_row)
    row = content['values']

    name.set(row[0])
    id_val.set(row[1])
    section.set(row[2])
    gender.set(row[3])

def clear_function():

    name.set("")
    id_val.set("")
    section.set("")
    gender.set("")

def update_function():

    conn = pymysql.connect(host="localhost", user="root", password="", database="student management system")
    curr = conn.cursor()
    curr.execute("Update data set name=%s, section=%s, gender=%s where id=%s", (name.get(), section.get(), gender.get(), id_val.get()))
    conn.commit()
    connect_data()
    conn.close()

def delete_function():
    conn = pymysql.connect(host="localhost", user="root", password="", database="student management system")
    curr = conn.cursor()
    curr.execute("Delete from data where id=%s", (id_val.get()))
    conn.commit()
    connect_data()
    conn.close()


# Button....

button_frame = tk.Frame(detail_frame, background="lightgrey")
button_frame.place(x=65, y=250, width=288, height=135)

add_button = tk.Button(button_frame, text="Add", font=("Arial", 18, "bold"), background="lightgrey", border=5, width=8, command=add_function)
add_button.grid(row=0, column=0, padx=2, pady=2)

update_button = tk.Button(button_frame, text="Update", font=("Arial", 18, "bold"), background="lightgrey", border=5, width=8, command=update_function)
update_button.grid(row=0, column=1, padx=2, pady=2)

delete_button = tk.Button(button_frame, text="Delete", font=("Arial", 18, "bold"), background="lightgrey", border=5, width=8, command=delete_function)
delete_button.grid(row=1, column=0, padx=5, pady=15)

clear_button = tk.Button(button_frame, text="Clear", font=("Arial", 18, "bold"), background="lightgrey", border=5, width=8, command=clear_function)
clear_button.grid(row=1, column=1, padx=2, pady=15)

# Search....

search_frame = tk.Frame(data_frame, background="lightgrey", border=10, relief=tk.GROOVE)
search_frame.pack(side=tk.TOP, fill=tk.X)

search_label = tk.Label(search_frame, text="Main Monitor", background="lightgrey", font=("Arial", 25, "bold"))
search_label.grid(row=0, column=0, padx=2, pady=2)


# Frame....

main_frame = tk.Frame(data_frame, background="lightgrey", border=10, relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH, expand=1)

y_scroll = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
x_scroll = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

monitor = ttk.Treeview(main_frame, columns=("Name", "ID", "Section", "Gender"), yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

y_scroll.config(command=monitor.yview)
y_scroll.pack(side=tk.RIGHT, fill=tk.Y)

x_scroll.config(command=monitor.xview)
x_scroll.pack(side=tk.BOTTOM, fill=tk.X)

monitor.heading("Name", text="Name")
monitor.heading("ID", text="ID")
monitor.heading("Section", text="Section")
monitor.heading("Gender", text="Gender")
monitor['show'] = 'headings'

monitor.pack(fill=tk.BOTH, expand=1)

connect_data()
monitor.bind("<ButtonRelease-1>", fetch_data)

sms.mainloop()