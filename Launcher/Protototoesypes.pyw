import os
import sys
import platform
import subprocess
import threading
import urllib.request
import json
import customtkinter as ctk
import tkinter.messagebox as messagebox  # <- Added import for standard messagebox

from PIL import Image

ctk.set_appearance_mode("dark")  # system, light, dark
ctk.set_default_color_theme("blue")  # use built-in blue theme

USER_HOME = os.path.expanduser("~")
INSTALL_DIR_MAIN = os.path.join(USER_HOME, "CheatSpyInstaller")
INSTALL_DIR_DEV = os.path.join(USER_HOME, "CheatSpyInstallerDev")
LOGIN_DATA_PATH = os.path.join(USER_HOME, "Cheatspydata.json")
ICON_URL = "https://raw.githubusercontent.com/OptionallyBlueStudios/CheatSpy/refs/heads/main/assets/icons/516x516.png"
ICON_PATH = os.path.join(USER_HOME, "CheatSpyInstaller", "icon.png")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def download_icon():
    ensure_dir(os.path.dirname(ICON_PATH))
    if not os.path.exists(ICON_PATH):
        try:
            urllib.request.urlretrieve(ICON_URL, ICON_PATH)
        except Exception as e:
            print(f"Failed to download icon: {e}")

class LoginWindow(ctk.CTkToplevel):
    def __init__(self, master, install_dir, is_dev=False):
        super().__init__(master)
        self.master = master
        self.install_dir = install_dir
        self.is_dev = is_dev
        self.title("CheatSpy Dev Login" if is_dev else "CheatSpy Login")
        self.geometry("400x300")
        self.resizable(False, False)

        # Set window icon if available
        if os.path.exists(ICON_PATH):
            try:
                self.iconbitmap(ICON_PATH)
            except Exception:
                pass

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=15, padx=20)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=15, padx=20)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.attempt_login)
        self.login_button.pack(pady=20)

        # Autocreate dev login file if needed
        if is_dev:
            self.create_dev_login_file()

    def create_dev_login_file(self):
        login_file = os.path.join(self.install_dir, "dev_login.txt")
        if not os.path.exists(login_file):
            ensure_dir(self.install_dir)
            with open(login_file, "w") as f:
                f.write("devuser\ndevpass\n")
            print(f"Created default dev login file at {login_file}")

    def attempt_login(self):
        entered_user = self.username_entry.get().strip()
        entered_pass = self.password_entry.get().strip()

        if self.is_dev:
            dev_login_file = os.path.join(self.install_dir, "dev_login.txt")
            if not os.path.exists(dev_login_file):
                messagebox.showerror(title="Error", message="Dev login file missing!")
                return

            try:
                with open(dev_login_file, "r") as f:
                    lines = f.read().splitlines()
                if len(lines) < 2:
                    messagebox.showerror(title="Error", message="Dev login file corrupted!")
                    return

                dev_user, dev_pass = lines[0].strip(), lines[1].strip()

                if entered_user == dev_user and entered_pass == dev_pass:
                    self.master.save_login(entered_user, entered_pass)
                    messagebox.showinfo(title="Success", message="Login successful!")
                    self.destroy()
                    self.master.run_script(os.path.join(self.install_dir, "CheatSpy-App", "gui.py"))
                else:
                    messagebox.showerror(title="Login Failed", message="Invalid username or password.")
            except Exception as e:
                messagebox.showerror(title="Error", message=f"Failed to read dev login file:\n{e}")
        else:
            # For non-dev login, just save and run main
            self.master.save_login(entered_user, entered_pass)
            messagebox.showinfo(title="Success", message="Login successful!")
            self.destroy()
            self.master.run_script(os.path.join(self.install_dir, "CheatSpy-App", "gui.py"))

class CheatSpyLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CheatSpy Launcher")
        self.geometry("600x400")
        self.resizable(False, False)
        download_icon()

        if os.path.exists(ICON_PATH):
            try:
                self.iconbitmap(ICON_PATH)
            except Exception:
                pass

        # Style colors
        self.configure(fg_color="#121212")
        self.color_orange = "#FFA500"

        self.label = ctk.CTkLabel(self, text="CheatSpy Launcher", font=ctk.CTkFont(size=24, weight="bold"))
        self.label.pack(pady=(30,20))

        self.login_main_btn = ctk.CTkButton(self, text="Open Main", width=200, command=self.open_main)
        self.login_main_btn.pack(pady=10)

        self.login_dev_btn = ctk.CTkButton(self, text="Open Dev (with Login)", width=200, command=self.open_dev_login)
        self.login_dev_btn.pack(pady=10)

        self.login_saved_btn = ctk.CTkButton(self, text="Open Dev (Auto Login)", width=200, command=self.auto_login_dev)
        self.login_saved_btn.pack(pady=10)

    def open_main(self):
        self.run_script(os.path.join(INSTALL_DIR_MAIN, "CheatSpy-App", "gui.py"))

    def open_dev_login(self):
        LoginWindow(self, INSTALL_DIR_DEV, is_dev=True)

    def auto_login_dev(self):
        login_data = self.load_login()
        if not login_data:
            messagebox.showerror(title="Error", message="No saved login found. Please login first.")
            return

        username = login_data.get("username", "")
        password = login_data.get("password", "")
        dev_login_file = os.path.join(INSTALL_DIR_DEV, "dev_login.txt")

        try:
            with open(dev_login_file, "r") as f:
                lines = f.read().splitlines()
            if len(lines) < 2:
                messagebox.showerror(title="Error", message="Dev login file corrupted!")
                return

            dev_user, dev_pass = lines[0].strip(), lines[1].strip()
            if username == dev_user and password == dev_pass:
                self.run_script(os.path.join(INSTALL_DIR_DEV, "CheatSpy-App", "gui.py"))
            else:
                messagebox.showerror(title="Login Failed", message="Saved credentials are invalid.")
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Failed to read dev login file:\n{e}")

    def save_login(self, username, password):
        data = {"username": username, "password": password}
        try:
            with open(LOGIN_DATA_PATH, "w") as f:
                json.dump(data, f)
            print(f"Saved login to {LOGIN_DATA_PATH}")
        except Exception as e:
            print(f"Failed to save login: {e}")

    def load_login(self):
        if os.path.exists(LOGIN_DATA_PATH):
            try:
                with open(LOGIN_DATA_PATH, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load login data: {e}")
        return None

    def run_script(self, script_path):
        if not os.path.exists(script_path):
            messagebox.showerror(title="Error", message=f"Script not found:\n{script_path}")
            return

        # Run script in a new process
        try:
            subprocess.Popen([sys.executable, script_path])
            self.destroy()
        except Exception as e:
            messagebox.showerror(title="Error", message=f"Failed to run script:\n{e}")

if __name__ == "__main__":
    app = CheatSpyLauncher()
    app.mainloop()
