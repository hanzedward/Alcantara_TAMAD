import pygame
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3

pygame.mixer.init()

def on_subject_click(event):
    if subject_entry.get() == "Enter your subject:":
        subject_entry.delete(0, tk.END)
        subject_entry.config(fg="black")

def on_subject_focusout(event):
    if subject_entry.get() == "":
        subject_entry.insert(0, "Enter your subject:")
        subject_entry.config(fg="gray")

def on_task_click(event):
    if task_entry.get() == "Enter your task below:":
        task_entry.delete(0, tk.END)
        task_entry.config(fg="black")

def on_task_focusout(event):
    if task_entry.get() == "":
        task_entry.insert(0, "Enter your task below:")
        task_entry.config(fg="gray")

music_playing = False
is_dark_mode = True
menu_open = False

def toggle_music():
    global music_playing
    if music_playing:
        pygame.mixer.music.stop()
        music_playing = False
    else:
        pygame.mixer.music.load("Download.mp3")
        pygame.mixer.music.play(loops=-1, start=0.0)
        music_playing = True

def switch_screen(show, hide):
    hide.pack_forget()
    show.pack(fill="both", expand=True)
    if show == screen_2:
        root.geometry("700x500")
        hide_buttons()
    elif show == screen_3:
        root.geometry("700x500")
        hide_buttons()
    else:
        root.geometry("500x500")
        hide_buttons()

def create_db():
    conn = sqlite3.connect('tasks_manager.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS student_tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task TEXT NOT NULL,
            due_date TEXT NOT NULL,
            due_time TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS task_list (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            subject TEXT, 
            task TEXT, 
            due_date TEXT, 
            due_time TEXT, 
            done INTEGER DEFAULT 0, 
            FOREIGN KEY (task_id) REFERENCES student_tasks(task_id)
        )
    ''')
   
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            task TEXT NOT NULL,
            due_date TEXT NOT NULL,
            due_time TEXT NOT NULL,
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

create_db()

create_db()

def save_task():
    subject = subject_entry.get()
    task = task_entry.get()
    due_date = f"{day_combobox.get()}/{month_combobox.get()}/{year_combobox.get()}"
    due_time = time_combobox.get()

    if subject == "Enter your subject:" or subject == "" or task == "Enter your task below:" or task == "":
        messagebox.showwarning("Input Error", "Please enter both subject and task before saving!")
    else:
        conn = sqlite3.connect('tasks_manager.db')
        c = conn.cursor()

        c.execute('''
            INSERT INTO student_tasks (subject, task, due_date, due_time)
            VALUES (?, ?, ?, ?)
        ''', (subject, task, due_date, due_time))

        conn.commit()
        conn.close()

        task_listbox.insert(tk.END, f"{subject} - {task} - {due_date} - {due_time}")
        day_combobox.set('')
        month_combobox.set('')
        year_combobox.set('')
        time_combobox.set('00:00')
        subject_entry.delete(0, tk.END)
        task_entry.delete(0, tk.END)


def load_tasks():
    conn = sqlite3.connect('tasks_manager.db')
    c = conn.cursor()

    c.execute('''
        SELECT subject, task, due_date, due_time FROM student_tasks
    ''')

    tasks = c.fetchall()
    conn.close()

    for task in tasks:
        task_listbox.insert(tk.END, f"{task[0]} - {task[1]} - {task[2]} - {task[3]}")

def mark_task_done():
    selected_task_index = task_listbox.curselection()

    if not selected_task_index:
        messagebox.showwarning("No Task Selected", "Please select a task to mark as done!")
        return

    task_text = task_listbox.get(selected_task_index)

    if "✔" in task_text:
        messagebox.showinfo("Task Already Done", "This task is already marked as done.")
        return

    updated_task_text = f"{task_text} ✔"
    task_listbox.delete(selected_task_index)
    task_listbox.insert(selected_task_index, updated_task_text)

    task_details = task_text.split(' - ')
    subject_name = task_details[0]  
    task_description = task_details[1]

    conn = sqlite3.connect('tasks_manager.db')
    c = conn.cursor()

    c.execute('''SELECT task_id FROM student_tasks WHERE subject = ? AND task = ?''', (subject_name, task_description))
    result = c.fetchone()

    if result:
        task_id = result[0] 

        c.execute('''UPDATE student_tasks SET done = 1 WHERE task_id = ?''', (task_id,))
        conn.commit()
        conn.close()
    else:
        messagebox.showwarning("Error", "Task not found in the database.")

def load_history():
    conn = sqlite3.connect('tasks_manager.db')
    c = conn.cursor()

    c.execute('''
        SELECT subject, task, due_date, due_time, deleted_at FROM history
    ''')

    history = c.fetchall()
    conn.close()

    for record in history:
        history_listbox.insert(tk.END, f"{record[0]} - {record[1]} - {record[2]} - {record[3]} - Deleted at: {record[4]}")


def remove_task():
    selected_task_index = task_listbox.curselection()

    if not selected_task_index:
        messagebox.showwarning("No Task Selected", "Please select a task to remove!")
        return

    task = task_listbox.get(selected_task_index)
    
    if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete the task:\n{task}?"):
        history_listbox.insert(tk.END, task)
        task_listbox.delete(selected_task_index)

        conn = sqlite3.connect('tasks_manager.db')
        c = conn.cursor()

        subject, task_description, due_date, due_time = task.split(" - ")

        c.execute(''' 
            INSERT INTO history (subject, task, due_date, due_time)
            VALUES (?, ?, ?, ?) 
        ''', (subject, task_description, due_date, due_time))

        c.execute(''' 
            DELETE FROM student_tasks 
            WHERE subject = ? AND task = ? AND due_date = ? AND due_time = ? 
        ''', (subject, task_description, due_date, due_time))

        conn.commit()
        conn.close()


def go_home():
    switch_screen(screen_1, screen_2)

def toggle_menu():
    global menu_open
    if menu_open:
        hide_buttons()
    else:
        show_buttons()
    menu_open = not menu_open

def show_buttons():
    home_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
    mark_done_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    remove_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
    darklight_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew") 
    history_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

def hide_buttons():
    home_button.grid_forget()
    mark_done_button.grid_forget()
    remove_button.grid_forget()
    darklight_button.grid_forget()
    history_button.grid_forget()

def toggle_mode():
    global is_dark_mode
    if is_dark_mode:
        root.configure(bg="white")
        screen_2.configure(bg="white")
        task_listbox_frame.configure(bg="white", bd=2, relief="solid")
        inner_frame.configure(bg="white", bd=2, relief="solid")
        task_listbox.config(bg="white", fg="black")
        task_listbox_scrollbar.config(bg="white")
        mark_done_button.config(bg="white")
        remove_button.config(bg="white")
        home_button.config(bg="white")
        button_frame.configure(bg="white")
        tk.Label(inner_frame, text="GAWIN MO NA!!", font=("Helvetica", 16, "bold"), fg="black", bg="white").grid(row=0, column=0, columnspan=3, pady=10)
        update_darklight_button("light")
        is_dark_mode = False
        
    else:
        root.configure(bg="black")
        screen_2.configure(bg="black")
        task_listbox_frame.configure(bg="black", bd=2, relief="solid")
        inner_frame.configure(bg="black", bd=2, relief="solid")
        task_listbox.config(bg="black", fg="white")
        task_listbox_scrollbar.config(bg="black")
        mark_done_button.config(bg="black")
        remove_button.config(bg="black")
        home_button.config(bg="black")
        button_frame.configure(bg="black")
        tk.Label(inner_frame, text="GAWIN MO NA!!", font=("Helvetica", 16, "bold"), fg="white", bg="black").grid(row=0, column=0, columnspan=3, pady=10)
        update_darklight_button("dark")
        is_dark_mode = True

def update_darklight_button(mode):
    global darklight_photo
    img = Image.open("darklight.jpg")
    width, height = img.size

    left_img = img.crop((0, 0, width // 2, height)) 
    right_img = img.crop((width // 2, 0, width, height)) 

    if mode == "light":
        resized_img = left_img.resize((50, 50), Image.Resampling.LANCZOS)
        darklight_photo = ImageTk.PhotoImage(resized_img)
    else:
        resized_img = right_img.resize((50, 50), Image.Resampling.LANCZOS)
        darklight_photo = ImageTk.PhotoImage(resized_img)

    darklight_button.config(image=darklight_photo)

def reset_history():
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the history? This action cannot be undone."):
        history_listbox.delete(0, tk.END)
        messagebox.showinfo("Reset", "History has been reset!")


root = tk.Tk()
root.geometry("500x500")
root.title("TAMAD")

create_db()

screen_1 = tk.Frame(root, bg="white")
img = Image.open("image.gif").resize((500, 500), Image.Resampling.LANCZOS)
photo = ImageTk.PhotoImage(img)
canvas = tk.Canvas(screen_1, width=500, height=500)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=photo)

tk.Label(screen_1, text="MAY ACTIVITY NA NAMAN?!", font=("Helvetica", 15, "bold"), fg="#2E4053").place(x=130, y=50)

view_image = Image.open("view.jpg").resize((30, 30), Image.Resampling.LANCZOS)
view_photo = ImageTk.PhotoImage(view_image)
tk.Button(screen_1, image=view_photo, command=lambda: switch_screen(screen_2, screen_1), relief="raised", bd=3, bg="#f4f1e1").place(x=250, y=405)

subject_entry = tk.Entry(screen_1, font=("Arial", 10), width=30, bd=5, relief="sunken", fg="gray", bg="#f4f4f4")
subject_entry.place(x=10, y=365)
subject_entry.insert(0, "Enter your subject:")
subject_entry.bind("<FocusIn>", on_subject_click)
subject_entry.bind("<FocusOut>", on_subject_focusout)

save_image = Image.open("save_icon.png").resize((30, 30), Image.Resampling.LANCZOS)
save_photo = ImageTk.PhotoImage(save_image)
tk.Button(screen_1, command=save_task, image=save_photo, relief="raised", bd=2, padx=10, pady=5).place(x=250, y=365)

task_entry = tk.Entry(screen_1, font=("Arial", 10), width=30, bd=5, relief="sunken", fg="gray", bg="#f4f4f4")
task_entry.place(x=10, y=400)
task_entry.insert(0, "Enter your task below:")
task_entry.bind("<FocusIn>", on_task_click)
task_entry.bind("<FocusOut>", on_task_focusout)

due_date_label = tk.Label(screen_1, text="Due Date", font=("Arial", 10), bg="#f4f4f4")
due_date_label.place(x=10, y=435)

day_combobox = ttk.Combobox(screen_1, values=[str(i) for i in range(1, 32)], width=5, font=("Arial", 10))
day_combobox.place(x=10, y=455)

month_combobox = ttk.Combobox(screen_1, values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], width=6, font=("Arial", 10))
month_combobox.place(x=80, y=455)

year_combobox = ttk.Combobox(screen_1, values=[str(i) for i in range(2024, 2031)], width=6, font=("Arial", 10))
year_combobox.place(x=160, y=455)

time_combobox = ttk.Combobox(screen_1, values=[f"{h}:{m:02d}" for h in range(24) for m in [0, 30]], width=6, font=("Arial", 10))
time_combobox.set("00:00")
time_combobox.place(x=230, y=455)

play_image = Image.open("play.jpg").resize((30, 30), Image.Resampling.LANCZOS)
play_photo = ImageTk.PhotoImage(play_image)
play_button = tk.Button(screen_1, image=play_photo, command=toggle_music, relief="raised", bd=2, bg="white")
play_button.place(x=10, y=10)

screen_2 = tk.Frame(root, bg="black")

task_listbox_frame = tk.Frame(screen_2, bg="black", bd=5, relief="solid")
task_listbox_frame.pack(fill="both", expand=True, pady=40)

inner_frame = tk.Frame(task_listbox_frame, bg="black", bd=2, relief="solid", padx=10)
inner_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)

tk.Label(inner_frame, text="GAWIN MO NA!!", font=("Helvetica", 16, "bold"), fg="white", bg="black").grid(row=0, column=0, columnspan=3, pady=10)

task_listbox = tk.Listbox(inner_frame, width=60, height=16, font=("Arial", 12), selectmode=tk.SINGLE)
task_listbox.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
task_listbox_scrollbar = tk.Scrollbar(inner_frame, orient="vertical", command=task_listbox.yview)
task_listbox_scrollbar.grid(row=1, column=1, sticky="ns", padx=0)
task_listbox.config(yscrollcommand=task_listbox_scrollbar.set)
task_listbox_xscrollbar = tk.Scrollbar(task_listbox_frame, orient="horizontal", command=task_listbox.xview)
task_listbox_xscrollbar.grid(row=2, column=0, sticky="ew", padx=10)
task_listbox.config(xscrollcommand=task_listbox_xscrollbar.set)

mark_done_image = Image.open("markasdone.png").resize((50, 50), Image.Resampling.LANCZOS)
mark_done_photo = ImageTk.PhotoImage(mark_done_image)

remove_image = Image.open("remove.jpg").resize((50, 50), Image.Resampling.LANCZOS)
remove_photo = ImageTk.PhotoImage(remove_image)

home_image = Image.open("home.jpg").resize((50, 50), Image.Resampling.LANCZOS)
home_photo = ImageTk.PhotoImage(home_image)

menu_image = Image.open("menu.png").resize((50, 50), Image.Resampling.LANCZOS)
menu_photo = ImageTk.PhotoImage(menu_image)

history_image = Image.open("history.jpg").resize((50, 50), Image.Resampling.LANCZOS)
history_photo = ImageTk.PhotoImage(history_image)

menu_button = tk.Button(screen_2, image=menu_photo, command=toggle_menu, relief="raised", bd=2, bg="black")
menu_button.place(x=620, y=40)

button_frame = tk.Frame(screen_2, bg="black")
button_frame.place(x=610, y=100)

home_button = tk.Button(button_frame, image=home_photo, command=go_home, relief="raised", bd=2, bg="black")
mark_done_button = tk.Button(button_frame, image=mark_done_photo, command=mark_task_done, relief="raised", bd=2, bg="black")
remove_button = tk.Button(button_frame, image=remove_photo, command=remove_task, relief="raised", bd=2, bg="black")
history_button = tk.Button(button_frame, image=history_photo, command=lambda: switch_screen(screen_3, screen_2), relief="raised", bd=2, bg="black")

darklight_button = tk.Button(button_frame, relief="raised", bd=2, bg="black", command=toggle_mode)
hide_buttons()

update_darklight_button("dark")

load_tasks()

screen_1.pack(fill="both", expand=True)

screen_3 = tk.Frame(root, bg="pink")
tk.Label(screen_3, text="HISTORY DATABASE", font=("Helvetica", 18, "bold"), fg="white", bg="pink").pack(expand=True)

history_listbox = tk.Listbox(screen_3, width=70, height=15, font=("Arial", 12), selectmode=tk.SINGLE)
history_listbox.pack(padx=10, pady=20)

back_image = Image.open("back.jpg").resize((50, 50), Image.Resampling.LANCZOS)
back_photo = ImageTk.PhotoImage(back_image)
back_button = tk.Button(screen_3, image=back_photo, command=lambda: switch_screen(screen_2, screen_3), relief="raised", bd=2, bg="pink")
back_button.pack(pady=10)
back_button.image = back_photo

reset_image = Image.open("reset1.jpg").resize((50, 50), Image.Resampling.LANCZOS)
reset_photo = ImageTk.PhotoImage(reset_image)
reset_button = tk.Button(screen_3, image=reset_photo, command=reset_history, relief="raised", bd=2, bg="black")
reset_button.place(x=400, y=432)

root.mainloop()




