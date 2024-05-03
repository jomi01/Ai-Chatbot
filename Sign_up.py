import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image
import json 
import os
import re
import sys
import subprocess  # Ensure subprocess is imported

def sign_up_event():
    username = username_entry.get()
    reset_code = ''.join([var.get() for var in reset_code_vars])
    confirm_reset_code = ''.join([var.get() for var in confirm_reset_code_vars])

    if not is_username_unique(username):
        messagebox.showinfo(title="Username Taken", message="This username is already taken. Please choose another username.")
        return

    if reset_code != confirm_reset_code:
        messagebox.showinfo(title="Reset Code Mismatch", message="The reset codes entered do not match.")
        return

    if username and len(reset_code) == 4 and len(confirm_reset_code) == 4:
        user_data = {
            "username": username,
            "reset_code": reset_code
        }
        save_to_json(user_data)
        messagebox.showinfo(title="Registration Successful", message="New user registered successfully.")
        clear_form()
        
        # Close the current window and open the sign-in page
        app.destroy()
        subprocess.Popen(["python", "Sign_in.py"])  # Adjusted to correct format

    else:
        messagebox.showinfo(title="Incomplete Form", message="Please fill all fields correctly")

def is_username_unique(username):
    return not is_field_in_use("username", username)

def is_field_in_use(field, value):
    file_path = r"sign_up.json"
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            try:
                users = json.load(file)
                return any(user.get(field) == value for user in users)
            except json.JSONDecodeError:
                pass
    return False

def clear_form():
    username_entry.delete(0, 'end')
    for var in reset_code_vars:
        var.set("")
    for var in confirm_reset_code_vars:
        var.set("")

def save_to_json(data):
    file_path = r"sign_up.json"
    if not os.path.isfile(file_path):
        with open(file_path, 'w') as file:
            json.dump([], file)

    with open(file_path, 'r+') as file:
        try:
            file_data = json.load(file)
        except json.JSONDecodeError:
            file_data = []

        file_data.append(data)
        file.seek(0)
        file.truncate()
        json.dump(file_data, file, indent=4)

def on_reset_code_entry(*args):
    for i in range(4):
        current_text = reset_code_vars[i].get()
        numeric_text = ''.join(filter(str.isdigit, current_text))
        reset_code_vars[i].set(numeric_text[:1])
        if len(numeric_text) == 1 and i < 3:
            reset_code_entries[i+1].focus()

def on_confirm_reset_code_entry(*args):
    for i in range(4):
        current_text = confirm_reset_code_vars[i].get()
        numeric_text = ''.join(filter(str.isdigit, current_text))
        confirm_reset_code_vars[i].set(numeric_text[:1])
        if len(numeric_text) == 1 and i < 3:
            confirm_reset_code_entries[i+1].focus()

app = ctk.CTk()
app.geometry("800x480")

side_img_data = Image.open(r"assets/bit_logo.png")
user_icon_data = Image.open(r"assets/group.png")
reset_code_icon_data = Image.open(r"assets/change-password.png")
confirm_reset_code_icon_data = Image.open(r"assets/change-password.png")

side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 480))
user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(20, 20))
reset_code_icon = CTkImage(dark_image=reset_code_icon_data, light_image=reset_code_icon_data, size=(20, 20))
confirm_reset_code_icon = CTkImage(dark_image=confirm_reset_code_icon_data, light_image=confirm_reset_code_icon_data, size=(20, 20))

CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=400, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="BIT BUDDY", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
CTkLabel(master=frame, text="Sign Up", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
username_entry = ctk.CTkEntry(master=frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Security Code:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=reset_code_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
reset_code_frame = ctk.CTkFrame(master=frame, width=350, height=50, fg_color="#ffffff")
reset_code_frame.pack(anchor="w", padx=(25, 0))
reset_code_frame.pack_propagate(0)
reset_code_entries = []
reset_code_vars = []
for i in range(4):
    var = ctk.StringVar()
    entry = ctk.CTkEntry(master=reset_code_frame, width=40, height=40, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", textvariable=var)
    entry.pack(side="left", padx=10)
    var.trace("w", on_reset_code_entry)
    reset_code_entries.append(entry)
    reset_code_vars.append(var)

CTkLabel(master=frame, text="  Re-enter Security Code:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=confirm_reset_code_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
confirm_reset_code_frame = ctk.CTkFrame(master=frame, width=350, height=50, fg_color="#ffffff")
confirm_reset_code_frame.pack(anchor="w", padx=(25, 0))
confirm_reset_code_frame.pack_propagate(0)
confirm_reset_code_entries = []
confirm_reset_code_vars = []
for i in range(4):
    var = ctk.StringVar()
    entry = ctk.CTkEntry(master=confirm_reset_code_frame, width=40, height=40, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", textvariable=var)
    entry.pack(side="left", padx=10)  # Added the missing parenthesis here
    var.trace("w", on_confirm_reset_code_entry)
    confirm_reset_code_entries.append(entry)
    confirm_reset_code_vars.append(var)

CTkButton(command=sign_up_event, master=frame, text="Sign Up", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=350).pack(anchor="w", pady=(20, 0), padx=(25, 0))

app.mainloop()
