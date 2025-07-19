import subprocess
import webbrowser
import tkinter as tk
import tempfile
import os
import urllib.request
import sys
import ctypes

def install_package(package):
    # Show popup window during installation
    root = tk.Tk()
    root.title("Installer")
    label = tk.Label(root, text=f"Installing {package}...\nPlease wait.")
    label.pack(padx=20, pady=20)
    root.update()

    # Run pip install
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    # Close popup after installation
    root.destroy()

def check_and_install(package):
    try:
        __import__(package)
    except ImportError:
        install_package(package)

# Check and install pywebview if needed
try:
    import webview
except ImportError as e:
    check_and_install("pywebview")
    import webview

try:
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication
except ImportError as e:
    check_and_install("PyQt5")
    check_and_install("PyQtWebEngine")
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication

try:
    import qtpy
except ImportError as e:
    check_and_install("qtpy")

script_url = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/Installer/CheatSpy-v1.2-Installer.pyw"

temp_dir = tempfile.gettempdir()
temp_script_path = os.path.join(temp_dir, "CheatSpy-Installer-BlueHub-3jg7a8sgjmv32bjhm9631.pyw")

icon_url = "https://github.com/OptionallyBlueStudios/BlueHub/raw/refs/heads/main/icoicon.ico"

temp_icon_path = os.path.join(temp_dir, "BlueHub-PyWebView-Iconu3287gdsa43bhkjv6tdsa87i32qlfdsgajhf3.ico")

urllib.request.urlretrieve(icon_url, temp_icon_path)

def set_icon():
    app = QApplication.instance()
    if app:
        app.setWindowIcon(QIcon(temp_icon_path))

def set_taskbar_icon(icon_path):
    app = QApplication.instance()
    if app:
        # Set window icon (for title bar and alt-tab)
        app.setWindowIcon(QIcon(icon_path))

        # Windows 7+ taskbar icon fix
        myappid = 'mycompany.myproduct.subproduct.version'  # unique string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class API:
    def run_script(self):
        print("Script requested by frontend.")
        subprocess.Popen([sys.executable, "script.py"])
        return "Script launched."

    def openDiscord(self):
        print("Open Discord Requested.")
        webbrowser.open_new_tab('https://optb.short.gy/discord')
        return "Check your browser for the discord invite."

    def openGithub(self):
        print("Open GitHub Page Requested.")
        webbrowser.open_new_tab('https://github.com/OptionallyBlueStudios')
        return "Check your browser for the github page."

    def openCheatSpy(self):
        print("Open GitHub Page Requested.")
        webbrowser.open_new_tab('https://github.com/CheatSpy')
        return "Check your browser for the github page."

    def installCheatSpy(self):
        print("Installing CheatSpy")
        print(f"Downloading script from {script_url}...")
        urllib.request.urlretrieve(script_url, temp_script_path)
        print(f"Script saved to {temp_script_path}")
        print("Executing Script")
        subprocess.run([sys.executable, temp_script_path])

    def openCheatSpyApp(self):
        home_dir = os.path.expanduser("~")
        csins_dir = os.path.join(home_dir, "CheatSpyInstaller")
        csapp_dir = os.path.join(csins_dir, "CheatSpy-App")
        pythonfile_dir = os.path.join(csapp_dir, "gui.pyw")
        subprocess.run([sys.executable, pythonfile_dir])

if __name__ == '__main__':
    # Create the API instance once
    api = API()

    # Get screen dimensions for maximized window
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    # Create the webview window with the API object
    webview.create_window(
        title="BlueHub",
        url="https://optionallybluestudios.github.io/BlueHub",
        js_api=api,
        width=screen_width,
        height=screen_height,
        resizable=True,
        maximized=True,
    )

    webview.start(set_icon, gui='qt')
