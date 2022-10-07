from random import randint
from tkinter import *
from tkinter import messagebox
import json
from pyclip import copy

FONT_NAME = "Arial"
WHITE = "#FFFFFF"


# ------------------------------------------- TODO Generate Password ------------------------------------------------- #
def create_password(num_count, spec_count, password_length):
    password_digits = []
    password_spec_chars = []
    password_chars = []  # Not strictly necessary, clears "referenced before assignment" message
    while len(password_digits) != num_count or len(password_spec_chars) != spec_count:
        password_chars = [chr(randint(33, 126)) for _ in range(password_length)]
        password_digits = [char for char in password_chars if char.isdigit()]
        password_spec_chars = [char for char in password_chars if not char.isalnum()]
    return "".join(password_chars)


# ------------------------------------------- TODO JSON Data Handling ------------------------------------------------ #
def store_entry(web_name, username, password):
    new_entry = {web_name: {"Username": username, "Password": password}}
    try:
        with open("PasswordBank.json", "r") as password_bank:
            pw_bank = json.load(password_bank)
            pw_bank.update(new_entry)
        with open("PasswordBank.json", "w") as password_bank:
            json.dump(pw_bank, password_bank, indent=4)
    except FileNotFoundError:
        with open("PasswordBank.json", "w") as password_bank:
            json.dump(new_entry, password_bank, indent=4)


def get_entry(web_name):
    try:
        with open("PasswordBank.json", "r") as password_bank:
            password_dict = json.load(password_bank)
            try:
                return password_dict[web_name]
            except KeyError:
                pass
                # return {"Username": f"No entry for {error_message}", "Password": f"No entry for {error_message}"}
    except FileNotFoundError:
        store_entry("N/A", "N/A", "N/A")
        get_entry(web_name)


# ----------------------------------------- TODO Setup Window & Canvas ----------------------------------------------- #
# Create the window
window = Tk()
window.title("PassVault Password Manager")
window.config(padx=50, pady=50, bg=WHITE)
# End creation of the window

# Create the canvas and put the logo on the screen
canvas = Canvas(width=212, height=216, bg=WHITE, highlightthickness=0)
Logo = PhotoImage(file="Logo.png")
canvas.create_image(106, 108, image=Logo)
canvas.grid(row=0, column=0, columnspan=2)
# End canvas
# ----------------------------------------------- End Window/Canvas Setup -------------------------------------------- #

# ----------------------------------------------- Label Names and Widgets -------------------------------------------- #
# Name Block
name_label = Label(text="Name: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
name_label.grid(row=1, column=0, sticky='e')
name_input = Entry(width=20, relief="solid", exportselection=False)
name_input.grid(row=1, column=1, sticky='w')
name_input.focus()
# End name block

# Username Block
username_label = Label(text="Username: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
username_label.grid(row=2, column=0, sticky='e')
username_input = Entry(width=40, relief="solid", exportselection=False)
username_input.grid(row=2, column=1, sticky='w')
# End username block

# Password block
password_label = Label(text="Password: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
password_label.grid(row=3, column=0, sticky='e')
password_input = Entry(width=20, relief="solid")
password_input.grid(row=3, column=1, sticky='w')
# End password block

# Password parameters block
passwordLength_label = Label(text="Password Length: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
passwordLength_label.grid(row=4, column=0, sticky='e')
password_len = Spinbox(width=5, from_=8, to=20, relief="solid")
password_len.grid(row=4, column=1, sticky='w')

numNumbers_label = Label(text="Numbers: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
numNumbers_label.grid(row=5, column=0, sticky='e')
num_numbers = Spinbox(width=5, from_=2, to=5, relief="solid")
num_numbers.grid(row=5, column=1, sticky='w')

numSpecChars_label = Label(text="Special Characters: ", font=(FONT_NAME, 16, "normal"), bg=WHITE)
numSpecChars_label.grid(row=6, column=0, sticky='e')
num_specChars = Spinbox(width=5, from_=2, to=5, relief="solid")
num_specChars.grid(row=6, column=1, sticky='w')


# End password parameters block
# ----------------------------------------------- End Label Names Section -------------------------------------------- #


# ------------------------------------------ TODO Create Generate Password Button ------------------------------------ #
def generate_password():
    pass_length = int(password_len.get())
    password_input.delete(first=0, last=END)
    numbers = int(num_numbers.get())
    spec_chars = int(num_specChars.get())
    password = create_password(num_count=numbers, spec_count=spec_chars, password_length=pass_length)
    password_input.insert(0, password)
    copy(password)


# Password Button
gen_password = Button(text="Generate Password", command=generate_password, width=15)
gen_password.grid(row=3, column=1, sticky='e')


# --------------------------------------------- End Password Button Section ------------------------------------------ #


# ----------------------------------------------- Search Function Section -------------------------------------------- #
def search_entry():
    web_name = name_input.get()
    if get_entry(web_name) is not None:
        new_window = Toplevel(window)
        new_window.geometry('300x100')
        new_window.config(padx=35, pady=10)
        entry = get_entry(web_name)
        label_string = f"Entry for {web_name}\nUsername: {entry['Username']}\nPassword: {entry['Password']}"
        search_result = Label(new_window, text=label_string)
        search_result.grid(row=0, column=0, columnspan=3)

        copy_username = Button(new_window, text="Copy Username", command=lambda: copy(entry['Username']), width=15)
        copy_username.grid(row=1, column=0)

        copy_password = Button(new_window, text="Copy Password", command=lambda: copy(entry['Password']), width=15)
        copy_password.grid(row=1, column=2)
    else:
        messagebox.showinfo(title="Error!", message=f"Sorry, there is no entry for {web_name}.")


# Search button
search_entries = Button(text="Search", command=search_entry, width=15)
search_entries.grid(row=1, column=1, sticky='e')
# --------------------------------------------- End Search Function Section ------------------------------------------ #


# -------------------------------------------- TODO Create Save Entry Button ----------------------------------------- #
def open_popup():
    name = name_input.get()
    username = username_input.get()
    password = password_input.get()
    new_window = Toplevel(window)
    new_window.geometry("500x150")

    def save_entry():
        save_name = name_input.get()
        save_username = username_input.get()
        save_password = password_input.get()
        store_entry(save_name, save_username, save_password)
        name_input.delete(first=0, last=END)
        username_input.delete(first=0, last=END)
        password_input.delete(first=0, last=END)
        new_window.destroy()

    def cancel():
        password_input.delete(first=0, last=END)
        new_window.destroy()

    if not (len(name) == 0 or len(username) == 0 or len(password) == 0):
        new_window.config(padx=150, pady=50)
        new_window.title("Confirm Entry")
        prompt = Label(new_window, text="Would you like to save this password?")
        prompt.grid(row=0, column=0, columnspan=2)
        confirm_save = Button(new_window, text="Save", command=save_entry, width=15)
        confirm_save.grid(row=1, column=1)
        cancel = Button(new_window, text="Cancel", command=cancel, width=15)
        cancel.grid(row=1, column=0)

    else:
        new_window.config(padx=200, pady=50)
        new_window.title("Error")
        prompt = Label(new_window, text="Missing Entry!")
        prompt.grid(row=0, column=0)
        ok = Button(new_window, text="OK", command=new_window.destroy, width=15)
        ok.grid(row=1, column=0)


# Save Button
save = Button(text="Save Password", command=open_popup, width=60)
save.grid(row=7, column=0, columnspan=2)
# ----------------------------------------------- End Save Entry Section --------------------------------------------- #

window.mainloop()
