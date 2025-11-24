import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",      
        password="142800",      
        database="contactdb"
    )


def add_contact():
    name = name_var.get()
    phone = phone_var.get()
    email = email_var.get()

    if name == "" or phone == "" or email == "":
        messagebox.showwarning("Input Error", "All fields are required")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)",
                   (name, phone, email))
    db.commit()
    db.close()

    fetch_contacts()
    clear_fields()
    messagebox.showinfo("Success", "Contact added successfully")


def fetch_contacts():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    db.close()

    for row in contact_table.get_children():
        contact_table.delete(row)

    for row in rows:
        contact_table.insert("", "end", values=row)


def select_contact(event):
    selected = contact_table.focus()
    data = contact_table.item(selected)
    row = data['values']

    if row:
        id_var.set(row[0])
        name_var.set(row[1])
        phone_var.set(row[2])
        email_var.set(row[3])


def update_contact():
    cid = id_var.get()
    if cid == "":
        messagebox.showwarning("Select Error", "Select a contact to update")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE contacts SET name=%s, phone=%s, email=%s WHERE id=%s",
                   (name_var.get(), phone_var.get(), email_var.get(), cid))
    db.commit()
    db.close()

    fetch_contacts()
    clear_fields()
    messagebox.showinfo("Updated", "Contact updated successfully")



def delete_contact():
    cid = id_var.get()
    if cid == "":
        messagebox.showwarning("Select Error", "Select a contact to delete")
        return

    db = connect_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=%s", (cid,))
    db.commit()
    db.close()

    fetch_contacts()
    clear_fields()
    messagebox.showinfo("Deleted", "Contact deleted successfully")


def clear_fields():
    id_var.set("")
    name_var.set("")
    phone_var.set("")
    email_var.set("")


def reset_all_data():
    confirm = messagebox.askyesno("Confirm Reset", "Are you sure you want to delete ALL contacts?")
    if confirm:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM contacts")
        db.commit()
        db.close()

        fetch_contacts()
        clear_fields()
        messagebox.showinfo("Reset", "All contact data has been deleted!")

        
def reset_all_data():
    confirm = messagebox.askyesno(
        "Confirm Reset",
        "Are you sure you want to delete ALL contacts and reset ID numbers?"
    )

    if confirm:
        db = connect_db()
        cursor = db.cursor()

    
        cursor.execute("DELETE FROM contacts")

        
        cursor.execute("ALTER TABLE contacts AUTO_INCREMENT = 1")

        db.commit()
        db.close()

        fetch_contacts()
        clear_fields()
        messagebox.showinfo("Reset", "All contacts deleted and ID reset!")



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Modern Contact Management System")
root.geometry("800x550")



id_var = ctk.StringVar()
name_var = ctk.StringVar()
phone_var = ctk.StringVar()
email_var = ctk.StringVar()



title = ctk.CTkLabel(root, text="📇 Contact Management System",
                     font=("Arial", 28, "bold"))
title.pack(pady=15)



form_frame = ctk.CTkFrame(root, corner_radius=15)
form_frame.pack(pady=10, padx=20, fill="x")

ctk.CTkLabel(form_frame, text="Name:", font=("Arial", 16)).grid(row=0, column=0, padx=20, pady=10)
ctk.CTkEntry(form_frame, textvariable=name_var, width=250).grid(row=0, column=1, pady=10)

ctk.CTkLabel(form_frame, text="Phone:", font=("Arial", 16)).grid(row=1, column=0, padx=20, pady=10)
ctk.CTkEntry(form_frame, textvariable=phone_var, width=250).grid(row=1, column=1, pady=10)

ctk.CTkLabel(form_frame, text="Email:", font=("Arial", 16)).grid(row=2, column=0, padx=20, pady=10)
ctk.CTkEntry(form_frame, textvariable=email_var, width=250).grid(row=2, column=1, pady=10)


btn_frame = ctk.CTkFrame(root, corner_radius=15)
btn_frame.pack(pady=10)

ctk.CTkButton(btn_frame, text="Add", width=150, command=add_contact).grid(row=0, column=0, padx=10)
ctk.CTkButton(btn_frame, text="Update", width=150, command=update_contact).grid(row=0, column=1, padx=10)
ctk.CTkButton(btn_frame, text="Delete", width=150, fg_color="red", hover_color="#b30000", command=delete_contact).grid(row=0, column=2, padx=10)
ctk.CTkButton(btn_frame, text="Clear", width=150, fg_color="green", hover_color="#12e296",command=clear_fields).grid(row=0, column=3, padx=10)
ctk.CTkButton(btn_frame, text="Reset All Data", width=150, fg_color="orange", hover_color="#e67300", command=reset_all_data).grid(row=0, column=4, padx=10)



table_frame = ctk.CTkFrame(root)
table_frame.pack(pady=10, fill="both", expand=True)

columns = ("ID", "Name", "Phone", "Email")
contact_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)

for col in columns:
    contact_table.heading(col, text=col)
    contact_table.column(col, width=150)

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview",
                background="#1e1e1e",
                foreground="white",
                rowheight=30,
                fieldbackground="#1e1e1e")
style.map("Treeview",
          background=[("selected", "#0a84ff")])

contact_table.pack(fill="both", expand=True)
contact_table.bind("<ButtonRelease-1>", select_contact)


fetch_contacts()
root.mainloop()
