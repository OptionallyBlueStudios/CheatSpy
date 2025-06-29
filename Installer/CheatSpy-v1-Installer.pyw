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

def ensure_package(pkg_name, import_name=None):
    """Ensure a package is installed and importable, else install it."""
    import_name = import_name or pkg_name
    try:
        importlib.import_module(import_name)
    except ImportError:
        print(f"{pkg_name} not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg_name])

# Ensure Pillow and pywin32 if on Windows
ensure_package("Pillow", "PIL")
if platform.system() == "Windows":
    ensure_package("pywin32")

# Now safe to import those
from PIL import Image

# For Windows shortcut creation
if platform.system() == "Windows":
    try:
        import pythoncom
        from win32com.shell import shell, shellcon
        from win32com.client import Dispatch
        WIN32_AVAILABLE = True
    except ImportError:
        WIN32_AVAILABLE = False
else:
    WIN32_AVAILABLE = False

CHEATSY_ZIP_URL = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/ZIPs/Latest.zip"
REQUIREMENTS_URL = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/CheatSpy-App/requirements.txt"
ICON_URL = "https://raw.githubusercontent.com/OptionallyBlueStudios/CheatSpy/refs/heads/main/assets/icons/516x516.png"

class InstallerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CheatSpy Installer")
        self.geometry("500x480")
        self.resizable(False, False)

        self.icon_path = None
        self.set_window_icon()

        self.label = tk.Label(self, text="Welcome to CheatSpy Installer v1", font=("Arial", 14))
        self.label.pack(pady=10)

        self.install_button = tk.Button(self, text="Install CheatSpy", command=self.start_install_thread, width=20)
        self.install_button.pack(pady=10)

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
                img.save(ico_path, format='ICO', sizes=[(64,64)])
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

    def create_windows_shortcut(self, target_path, shortcut_path, icon_path):
        try:
            if not WIN32_AVAILABLE:
                self.log_message("pywin32 not available, skipping shortcut creation.")
                return

            shell_link = Dispatch('WScript.Shell').CreateShortcut(shortcut_path)
            shell_link.TargetPath = sys.executable  # Run with python.exe
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
        try:
            self.log_message("Detecting OS...")
            os_name = platform.system()
            self.log_message(f"OS Detected: {os_name}")

            home_dir = os.path.expanduser("~")
            install_dir = os.path.join(home_dir, "CheatSpyInstaller")
            os.makedirs(install_dir, exist_ok=True)

            zip_path = os.path.join(install_dir, "CSpy-Release-1.0.zip")

            self.log_message("Downloading CheatSpy ZIP...")
            urllib.request.urlretrieve(CHEATSY_ZIP_URL, zip_path)
            self.log_message("Download complete!")

            self.log_message("Extracting ZIP...")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(install_dir)
            self.log_message("Extraction complete!")

            # Download requirements.txt
            requirements_path = os.path.join(install_dir, "requirements.txt")
            self.log_message("Downloading requirements.txt...")
            urllib.request.urlretrieve(REQUIREMENTS_URL, requirements_path)
            self.log_message("requirements.txt downloaded!")

            self.log_message("Installing required packages...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path],
                                    capture_output=True, text=True)
            self.log_message(result.stdout)
            if result.returncode != 0:
                self.log_message("Error during package installation:")
                self.log_message(result.stderr)
                messagebox.showerror("Error", "Failed to install required packages. Check the log.")
                self.finish_install(failure=True)
                return

            self.log_message("All packages installed successfully!")

            # Create desktop shortcut (Windows only)
            desktop_path = os.path.join(home_dir, "Desktop")
            target_script = os.path.join(install_dir, "CheatSpy-App", "gui.pyw")
            shortcut_path = os.path.join(desktop_path, "CheatSpy.lnk")

            if os_name == "Windows":
                self.log_message("Creating desktop shortcut...")
                self.create_windows_shortcut(target_script, shortcut_path, self.icon_path)
            else:
                # On macOS/Linux: create simple shortcut file on Desktop
                shortcut_txt_path = os.path.join(desktop_path, "CheatSpy.desktop")
                with open(shortcut_txt_path, "w") as f:
                    f.write(f"[Desktop Entry]\nName=CheatSpy\nExec=python3 \"{target_script}\"\nType=Application\n")
                self.log_message(f"Shortcut created at: {shortcut_txt_path} (manual icon needed)")

            self.log_message(f"CheatSpy installed successfully in {install_dir}")
            messagebox.showinfo("Success", f"CheatSpy installed successfully in:\n{install_dir}")

        except Exception as e:
            self.log_message(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred:\n{e}")

        self.finish_install()

    def finish_install(self, failure=False):
        self.install_button.config(state='normal')
        self.quit_button.config(state='normal')
        if failure:
            self.log_message("Installation failed.")
        else:
            self.log_message("Installation finished.")

if __name__ == "__main__":
    app = InstallerApp()
    app.mainloop()
