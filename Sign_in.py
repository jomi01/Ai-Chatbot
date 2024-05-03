import customtkinter as ctk
from customtkinter import *
from tkinter import messagebox
from PIL import Image
import json
import os
import subprocess

def sign_in_event():
    reset_code = ''.join([var.get() for var in reset_code_vars])
    username = username_entry.get()

    if check_credentials(username, reset_code):
        # Credentials are correct, open the chatbot page
        messagebox.showinfo("Login Successful")
        app.destroy()
        subprocess.Popen(["python", r"chatapp.py"])
    else:
        messagebox.showinfo("Login Failed", "Invalid username or Security Code. Please try again.")

def check_credentials(username, reset_code):
    file_path = r"sign_up.json"
    if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
            try:
                users = json.load(file)
                for user in users:
                    if user['username'] == username and user['reset_code'] == reset_code:
                        return True
            except json.JSONDecodeError:
                pass
    return False

def on_reset_code_entry(*args):
    for i in range(4):
        current_text = reset_code_vars[i].get()
        numeric_text = ''.join(filter(str.isdigit, current_text))
        reset_code_vars[i].set(numeric_text[:1])
        if len(numeric_text) == 1 and i < 3:
            reset_code_entries[i+1].focus()

app = ctk.CTk()
app.geometry("800x480")

side_img_data = Image.open(r"assets/bit_logo.png")
side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(400, 480))
CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

frame = CTkFrame(master=app, width=400, height=480, fg_color="#ffffff")
frame.pack_propagate(0)
frame.pack(expand=True, side="right")

CTkLabel(master=frame, text="Sign In", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))

CTkLabel(master=frame, text="  Username:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(21, 0), padx=(25, 0))
username_entry = ctk.CTkEntry(master=frame, width=350, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000")
username_entry.pack(anchor="w", padx=(25, 0))

CTkLabel(master=frame, text="  Security Code:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14)).pack(anchor="w", pady=(21, 0), padx=(25, 0))
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

CTkButton(command=sign_in_event, master=frame, text="Sign In", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12), text_color="#ffffff", width=350).pack(anchor="w", pady=(20, 0), padx=(25, 0))

app.mainloop()
