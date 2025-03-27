import sqlite3
import tkinter as tk
from tkinter import messagebox

# Create database and table
db = sqlite3.connect('data.db')
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)")
# вроде базу сделал, залью на гитхаб
cursor.execute("SELECT COUNT(*) FROM users")
if cursor.fetchone()[0] == 0:
    cursor.executemany("INSERT INTO users (name, age) VALUES (?, ?)", 
                       [('User_for_check_bd', 25)])
    db.commit()


# Functions
def show_data():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    user_data = "\n".join([f"ID: {u[0]}, Name: {u[1]}, Age: {u[2]}" for u in users])
    messagebox.showinfo("Users", user_data if user_data else "No data available.")


def insert_user(name, age, window):
    if not name or not age:
        messagebox.showerror("Error", "Please fill in all fields.")
        return
    try:
        cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", (name, int(age)))
        db.commit()
        messagebox.showinfo("Success", "User added successfully.")
        window.destroy()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def insert_data():
    window = tk.Toplevel(program)
    window.title('Insert User')
    window.geometry('300x200')

    lbl_name = tk.Label(window, text='Name:')
    lbl_name.pack(pady=5)
    name_entry = tk.Entry(window)
    name_entry.pack(pady=5)

    lbl_age = tk.Label(window, text='Age:')
    lbl_age.pack(pady=5)
    age_entry = tk.Entry(window)
    age_entry.pack(pady=5)

    btn_insert = tk.Button(window, text='Insert', command=lambda: insert_user(name_entry.get(), age_entry.get(), window))
    btn_insert.pack(pady=10)


def exit_program():
    db.close()
    messagebox.showinfo('Exit', 'Goodbye!')
    program.quit()

def delete_user_window():
    window = tk.Toplevel(program)
    window.title('Delete User')
    window.geometry('300x200')

    lbl_id = tk.Label(window, text='ID:')
    lbl_id.pack(pady=5)
    id_entry = tk.Entry(window)
    id_entry.pack(pady=5)

    btn_delete = tk.Button(window, text='Delete', command=lambda: delete_user_by_id(id_entry.get(), window))
    btn_delete.pack(pady=10)


def delete_user_by_id(user_id, window):
    if not user_id.isdigit():
        messagebox.showerror("Error", "Please enter a valid ID (number).")
        return
    cursor.execute("SELECT * FROM users WHERE id = ?", (int(user_id),))
    if cursor.fetchone() is None:
        messagebox.showerror("Error", f"No user with ID {user_id}")
        return
    cursor.execute("DELETE FROM users WHERE id = ?", (int(user_id),))
    db.commit()
    messagebox.showinfo("Success", f"User with ID {user_id} deleted successfully.")
    window.destroy()



# Main Program
program = tk.Tk()
program.title('Database')
program.geometry('400x200')

btn = tk.Button(program, text="Show Users", command=show_data)
btn.pack(pady=10)

btn_insert = tk.Button(program, text="Insert User", command=insert_data)
btn_insert.pack(pady=10)

btn_delete = tk.Button(program, text="Delete User", command=delete_user_window)
btn_delete.pack(pady=10)

btn_exit = tk.Button(program, text="Exit", command=exit_program)
btn_exit.pack(pady=10)

program.mainloop()

# вроде базу сделал, залью на гитхаб
# привет программист который читает, ты молодец, что читаешь комментарии, так держать!