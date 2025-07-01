import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import urllib.request
import os
import platform
import zipfile
import subprocess
import sys
import importlib

# --- Constants ---
CHEATSY_ZIP_URL = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/ZIPs/Latest.zip"
CHEATSPY_DEV_ZIP_URL = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/development/ZIPs/Latest.zip"
REQUIREMENTS_URL = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/CheatSpy-App/requirements.txt"
REQUIREMENTS_URL_DEV = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/development/CheatSpy-App/requirements.txt"
ICON_URL = "https://raw.githubusercontent.com/OptionallyBlueStudios/CheatSpy/refs/heads/main/assets/icons/516x516.png"
TOKENSERVICE = "http://141.147.118.157:5678/webhook/2eced3cf-68df-46d6-b30f-671771e30123"  # Replace with your webhook URL

# --- Ensure Required Packages ---
def ensure_package(pkg_name, import_name=None):
    import_name = import_name or pkg_name
    try:
        importlib.import_module(import_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])

ensure_package("requests")
ensure_package("Pillow", "PIL")
if platform.system() == "Windows":
    ensure_package("pywin32")

import requests
from PIL import Image

# --- Shortcut Setup for Windows ---
WIN32_AVAILABLE = False
if platform.system() == "Windows":
    try:
        import pythoncom
        from win32com.client import Dispatch
        WIN32_AVAILABLE = True
    except ImportError:
        WIN32_AVAILABLE = False

# --- Login Window ---
class LoginWindow(tk.Toplevel):
    def __init__(self, on_success_callback):
        super().__init__()
        self.title("Developer Login")
        self.geometry("300x180")
        self.resizable(False, False)
        self.on_success_callback = on_success_callback

        tk.Label(self, text="Username (Token):").pack(pady=(10, 0))
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(pady=5)

        tk.Label(self, text="Password (Pass):").pack(pady=(5, 0))
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(pady=5)

        self.login_button = tk.Button(self, text="Login", command=self.attempt_login)
        self.login_button.pack(pady=10)

        self.status_label = tk.Label(self, text="", fg="red")
        self.status_label.pack()

    def attempt_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            response = requests.get(
                TOKENSERVICE,
                params={"token": username, "pass": password},
                timeout=5
            )

            # Expecting: {"tf":"t"}
            data = response.json()
            if data.get("tf") == "t":
                self.destroy()
                self.on_success_callback()
            else:
                self.status_label.config(text="Invalid username or password.")
        except requests.exceptions.RequestException as e:
            self.status_label.config(text=f"Error: {e}")
        except ValueError:
            self.status_label.config(text="Invalid response format.")


# --- Installer GUI ---
class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CheatSpy Installer")
        self.geometry("500x480")
        self.resizable(False, False)

        self.icon_path = None
        self.set_window_icon()

        tk.Label(self, text="Welcome to CheatSpy Installer v1.1.2", font=("Arial", 14)).pack(pady=10)

        self.install_button = tk.Button(self, text="Install CheatSpy", command=self.start_install_thread, width=20)
        self.install_button.pack(pady=10)

        self.installdev_button = tk.Button(self, text="Install CheatSpy (DEV)", command=self.show_login, width=20)
        self.installdev_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", command=self.quit, width=20)
        self.quit_button.pack(pady=10)

        self.log = scrolledtext.ScrolledText(self, state='disabled', width=60, height=18)
        self.log.pack(pady=10)

    def log_message(self, message):
        self.log.config(state='normal')
        self.log.insert(tk.END, message + "\n")
        self.log.see(tk.END)
        self.log.config(state='disabled')

    def set_window_icon(self):
        try:
            home_dir = os.path.expanduser("~")
            icon_dir = os.path.join(home_dir, "CheatSpyInstaller")
            os.makedirs(icon_dir, exist_ok=True)
            png_path = os.path.join(icon_dir, "icon.png")
            ico_path = os.path.join(icon_dir, "icon.ico")

            if not os.path.exists(ico_path):
                urllib.request.urlretrieve(ICON_URL, png_path)
                img = Image.open(png_path)
                img.save(ico_path, format='ICO', sizes=[(64, 64)])
                self.icon_path = ico_path
            else:
                self.icon_path = ico_path

            if self.icon_path and os.path.exists(self.icon_path):
                self.iconbitmap(self.icon_path)
        except Exception as e:
            self.log_message(f"Failed to set window icon: {e}")

    def start_install_thread(self):
        self.install_button.config(state='disabled')
        self.quit_button.config(state='disabled')
        threading.Thread(target=self.install).start()

    def show_login(self):
        LoginWindow(on_success_callback=self.start_installdev_thread)

    def start_installdev_thread(self):
        self.installdev_button.config(state='disabled')
        self.quit_button.config(state='disabled')
        threading.Thread(target=self.installdev).start()

    def create_windows_shortcut(self, target_path, shortcut_path, icon_path):
        if not WIN32_AVAILABLE:
            self.log_message("pywin32 not available, skipping shortcut creation.")
            return

        try:
            shell_link = Dispatch('WScript.Shell').CreateShortcut(shortcut_path)
            shell_link.TargetPath = sys.executable
            shell_link.Arguments = f'"{target_path}"'
            shell_link.WorkingDirectory = os.path.dirname(target_path)
            if icon_path and os.path.exists(icon_path):
                shell_link.IconLocation = icon_path
            shell_link.Description = "CheatSpy GUI"
            shell_link.save()
            self.log_message(f"Shortcut created at: {shortcut_path}")
        except Exception as e:
            self.log_message(f"Failed to create shortcut: {e}")

    def install(self):
        self._run_install(zip_url=CHEATSY_ZIP_URL, req_url=REQUIREMENTS_URL)

    def installdev(self):
        self._run_install(zip_url=CHEATSPY_DEV_ZIP_URL, req_url=REQUIREMENTS_URL_DEV)

    def _run_install(self, zip_url, req_url):
        try:
            self.log_message("Detecting OS...")
            os_name = platform.system()
            self.log_message(f"OS Detected: {os_name}")

            home_dir = os.path.expanduser("~")
            install_dir = os.path.join(home_dir, "CheatSpyInstaller")
            os.makedirs(install_dir, exist_ok=True)
            zip_path = os.path.join(install_dir, "CSpy-Release.zip")

            self.log_message("Downloading CheatSpy ZIP...")
            urllib.request.urlretrieve(zip_url, zip_path)
            self.log_message("Download complete!")

            self.log_message("Extracting ZIP...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
            self.log_message("Extraction complete!")

            requirements_path = os.path.join(install_dir, "requirements.txt")
            self.log_message("Downloading requirements.txt...")
            urllib.request.urlretrieve(req_url, requirements_path)
            self.log_message("requirements.txt downloaded!")

            self.log_message("Installing required packages...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path],
                                    capture_output=True, text=True)
            self.log_message(result.stdout)
            if result.returncode != 0:
                self.log_message(result.stderr)
                messagebox.showerror("Error", "Failed to install required packages.")
                self.finish_install(failure=True)
                return

            desktop_path = os.path.join(home_dir, "Desktop")
            target_script = os.path.join(install_dir, "CheatSpy-App", "gui.py")
            shortcut_path = os.path.join(desktop_path, "CheatSpy.lnk")

            if os_name == "Windows":
                self.create_windows_shortcut(target_script, shortcut_path, self.icon_path)
            else:
                shortcut_txt_path = os.path.join(desktop_path, "CheatSpy.desktop")
                with open(shortcut_txt_path, "w") as f:
                    f.write(f"[Desktop Entry]\nName=CheatSpy\nExec=python3 \"{target_script}\"\nType=Application\n")
                self.log_message(f"Shortcut created at: {shortcut_txt_path} (manual icon needed)")

            self.log_message("CheatSpy installed successfully!")
            messagebox.showinfo("Success", f"CheatSpy installed successfully in:\n{install_dir}")
        except Exception as e:
            self.log_message(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")
        self.finish_install()

    def finish_install(self, failure=False):
        self.install_button.config(state='normal')
        self.installdev_button.config(state='normal')
        self.quit_button.config(state='normal')
        if failure:
            self.log_message("Installation failed.")
        else:
            self.log_message("Installation complete.")

# --- Entry Point ---
if __name__ == "__main__":
    InstallerApp().mainloop()
