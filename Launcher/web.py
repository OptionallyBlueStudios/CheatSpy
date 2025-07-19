import subprocess
import webbrowser
import tkinter as tk
import tempfile
import os
import subprocess
import urllib.request
import sys

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
        # Run the installation in main thread to show tkinter window properly
        install_package(package)

# Run check at script start
check_and_install("pywebview")

# Now you can import pywebview safely
import webview

script_url = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/Installer/CheatSpy-v1.2-Installer.pyw"

temp_dir = tempfile.gettempdir()
temp_script_path = os.path.join(temp_dir, "CheatSpy-Installer-BlueHub-3jg7a8sgjmv32bjhm9631.pyw")

# This is the Python object exposed to JavaScript
class API:
    def run_script(self):
        print("Script requested by frontend.")
        subprocess.Popen(["python", "script.py"], shell=True)
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
    api = API()
    
    # Load your live webpage
if __name__ == '__main__':
    # Create root window to get screen dimensions
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    api = API()

    # Create window maximized and set icon
    webview.create_window(
        title="BlueHub Launcher",
        url="https://optionallybluestudios.github.io/BlueHub",
        js_api=api,
        width=screen_width,
        height=screen_height,
        resizable=True,
    )
    
    webview.start()
