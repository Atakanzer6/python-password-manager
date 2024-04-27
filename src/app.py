import tkinter
import string
import secrets
import keyring
import pyperclip
import customtkinter as ct
from tkinter import messagebox
from keyring.errors import PasswordDeleteError


class App(ct.CTk):
    WIDTH = 780
    HEIGHT = 520
    FONT = ("Roboto Medium", 15)

    def __init__(self):
        super().__init__()

        #   -- Window --
        self.title("MyPass")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.minsize(App.WIDTH, App.HEIGHT)
        self.maxsize(App.WIDTH, App.HEIGHT)
        self.resizable(False, False)
        self.iconbitmap("../img/lock.ico")

        #   -- Frames --
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ct.CTkFrame(master=self, width=180, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ct.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", pady=20, padx=20)

        #   --Left Frame Config--
        self.frame_left.grid_rowconfigure(0, minsize=10)
        self.frame_left.grid_rowconfigure(5, weight=1)
        self.frame_left.grid_rowconfigure(8, minsize=20)
        self.frame_left.grid_rowconfigure(11, minsize=10)

        self.label_1 = ct.CTkLabel(master=self.frame_left, text="Options", text_font=("Roboto Medium", -16))
        self.label_1.grid(row=1, column=0, pady=10, padx=10)

        #   -- Left Frame Buttons --
        self.button_1 = ct.CTkButton(master=self.frame_left, text="Create Password", command=self.button_1_func)
        self.button_1.grid(row=2, column=0, pady=10, padx=20)

        self.button_2 = ct.CTkButton(master=self.frame_left, text="Find Password", command=self.button_2_func)
        self.button_2.grid(row=3, column=0, pady=10, padx=20)

        self.button_3 = ct.CTkButton(master=self.frame_left, text="Delete Password", fg_color="Darkred",
                                     hover_color="Red", command=self.button_3_func)
        self.button_3.grid(row=4, column=0, pady=10, padx=20)

        self.label_mode = ct.CTkLabel(master=self.frame_left, text="Appearance Mode:")
        self.label_mode.grid(row=9, column=0, pady=0, padx=10, sticky="w")

        self.option_menu = ct.CTkOptionMenu(master=self.frame_left, values=["Dark", "Light"], command=change_appearance)
        self.option_menu.grid(row=10, column=0, pady=0, padx=20, sticky="w")

        #   -- Right Frame Config --
        self.frame_right.grid_rowconfigure(3, weight=1)
        self.frame_right.grid_rowconfigure(7, weight=10)
        self.frame_right.grid_columnconfigure(1, weight=1)
        self.frame_right.grid_columnconfigure(2, weight=0)

        #   -- Image --
        self.canvas = ct.CTkCanvas(master=self.frame_right, width=200, height=200, highlightthickness=0, bg="#2a2d2e")
        self.img = tkinter.PhotoImage(file="../img/logo.png", )
        self.canvas.create_image(100, 100, image=self.img)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=2)

        #   -- Entries --
        self.website_entry = ct.CTkEntry(master=self.frame_right, width=280, placeholder_text="Website")
        self.website_entry.grid(row=2, column=0, columnspan=2, pady=5)

        self.email_entry = ct.CTkEntry(master=self.frame_right, width=280, placeholder_text="Email")
        self.email_entry.grid(row=3, column=0, columnspan=2, pady=5)

        self.password_entry = ct.CTkEntry(master=self.frame_right, width=280, placeholder_text="Password")
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        #   -- Entry Buttons --
        self.generate_button = ct.CTkButton(master=self.frame_right, text="Generate Password",
                                            command=self.generate_password, width=50)
        self.generate_button.grid(row=4, column=0, padx=5)

        self.button_4 = ct.CTkButton(master=self.frame_right, text="Save", width=280, command=self.set_password)
        self.button_4.grid(row=5, column=0, columnspan=2, pady=5, padx=10)

    def generate_password(self):
        special_char = "().-_"
        char = string.ascii_letters + string.digits + special_char
        password = "".join(secrets.choice(char) for _ in range(16))
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)

    def set_password(self):
        website = self.website_entry.get()
        username = self.email_entry.get()
        password = self.password_entry.get()
        if len(website) == 0 or len(username) == 0 or len(password) == 0:
            self.msgbox_blank_error()
        else:
            keyring.set_password(website, username, password)
            self.del_entries()
            messagebox.showinfo(title="MyPass", message="Your password has been saved.")

    def get_password(self):

        website = self.website_entry.get()
        email = self.email_entry.get()
        if len(website) == 0 or len(email) == 0:
            self.msgbox_blank_error()
        else:
            password = keyring.get_password(website, email)
            if password is None:
                self.msgbox_not_found_error()
            else:
                self.pop_up(email=email, password=password)
                self.del_entries()

    def del_password(self):
        try:
            website = self.website_entry.get()
            username = self.email_entry.get()
            if len(website) == 0 or len(username) == 0:
                self.msgbox_blank_error()
            else:
                keyring.delete_password(website, username)
                messagebox.showinfo(title="MyPass", message="You password has been deleted.")
                self.del_entries()
        except PasswordDeleteError:
            self.msgbox_not_found_error()

    def button_1_func(self):
        self.del_entries()
        self.generate_button.grid(row=4, column=0, padx=5)
        self.password_entry.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        self.button_4.configure(text="Save", fg_color="#1f6aa5", hover_color="#144870", command=self.set_password)

    def button_2_func(self):
        self.del_entries()
        self.generate_button.grid_forget()
        self.password_entry.grid_forget()
        self.button_4.configure(text="Find", fg_color="#1f6aa5", hover_color="#144870", command=self.get_password)

    def button_3_func(self):
        self.del_entries()
        self.generate_button.grid_forget()
        self.password_entry.grid_forget()
        self.button_4.configure(text="Delete", fg_color="Darkred", hover_color="red", command=self.del_password)

    def del_entries(self):
        self.website_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
        self.password_entry.delete(0, "end")

    def pop_up(self, email, password):
        def copy_password():
            pyperclip.copy(password)

        popup_width = 300
        popup_height = 200

        popup = ct.CTkToplevel(master=self.frame_right)
        popup.geometry(f"{popup_width}x{popup_height}")
        popup.minsize(popup_width, popup_height)
        popup.maxsize(popup_width, popup_height)
        popup.configure(pady=10, padx=10)
        popup.iconbitmap("../img/lock.ico")

        popup.title("MyPass")
        label = ct.CTkLabel(master=popup, text=f"Email: {email}\nPassword: ******")
        label.configure(pady=10, padx=10)
        label.pack()

        copy_btn = ct.CTkButton(master=popup, text="copy", command=copy_password)
        copy_btn.configure(pady=10, padx=10)
        copy_btn.pack()

        exit_btn = ct.CTkButton(master=popup, text="exit", command=popup.destroy)
        exit_btn.configure(pady=10, padx=10)
        exit_btn.pack()

    @staticmethod
    def msgbox_blank_error():
        messagebox.showinfo(title="Error", message="Please don't leave any blank spaces.")

    @staticmethod
    def msgbox_not_found_error():
        messagebox.showinfo(title="Error", message="Password not found.Please check your spelling and try again")


def change_appearance(new_appearance_mode):
    # change background of the canvas according to the theme
    ct.set_appearance_mode(new_appearance_mode)
    if new_appearance_mode == "Light":
        app.canvas.configure(background="#d1d5d8")
    else:
        app.canvas.configure(background="#2a2d2e")


if __name__ == "__main__":
    app = App()
    app.mainloop()
