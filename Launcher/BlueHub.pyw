import subprocess
import webbrowser
import tkinter as tk
import tempfile
import os
import urllib.request
import sys
import ctypes
import threading

version = 2.5 # CHANGE AT BOTTOM

def install_package(package):
    def do_install():
        root = tk.Tk()
        root.title("Installer")
        label = tk.Label(root, text=f"Installing {package}...\nPlease wait.")
        label.pack(padx=20, pady=20)
        root.update()
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        except Exception as e:
            label.config(text=f"Failed to install {package}:\n{e}")
            root.update()
            root.after(3000, root.destroy)
            root.mainloop()
        else:
            root.destroy()
    t = threading.Thread(target=do_install)
    t.start()
    t.join()

def check_and_install(package):
    try:
        __import__(package)
    except ImportError:
        install_package(package)

# Check and install pywebview if needed
try:
    import webview
except ImportError:
    check_and_install("pywebview")
    import webview

try:
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication
except ImportError:
    check_and_install("PyQt5")
    check_and_install("PyQtWebEngine")
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QApplication

try:
    import qtpy
except ImportError:
    check_and_install("qtpy")

script_url = "https://github.com/OptionallyBlueStudios/CheatSpy/raw/refs/heads/main/Installer/CheatSpy-v1.2-Installer.pyw"

temp_dir = tempfile.gettempdir()
temp_script_path = os.path.join(temp_dir, "CheatSpy-Installer-BlueHub-3jg7a8sgjmv32bjhm9631.pyw")

icon_url = "https://github.com/OptionallyBlueStudios/BlueHub/raw/refs/heads/main/icoicon.ico"
temp_icon_path = os.path.join(temp_dir, "BlueHub-PyWebView-Iconu3287gdsa43bhkjv6tdsa87i32qlfdsgajhf3.ico")

def download_icon():
    if not os.path.exists(temp_icon_path):
        try:
            urllib.request.urlretrieve(icon_url, temp_icon_path)
        except Exception as e:
            print(f"Failed to download icon: {e}")

download_icon()

def set_icon():
    app = QApplication.instance()
    if app and os.path.exists(temp_icon_path):
        app.setWindowIcon(QIcon(temp_icon_path))

def set_taskbar_icon(icon_path):
    app = QApplication.instance()
    if app and os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
        myappid = 'optionallyblue.bluehub.pywebapp.version3public'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception as e:
            print(f"Failed to set taskbar icon: {e}")

class API:

    def openDiscord(self):
        threading.Thread(target=webbrowser.open_new_tab, args=('https://optb.short.gy/discord',)).start()
        return "Check your browser for the discord invite."

    def OpenURL_INT(self, url):
        threading.Thread(target=webbrowser.open_new_tab, args=(url,)).start()

    def openGithub(self):
        threading.Thread(target=webbrowser.open_new_tab, args=('https://github.com/OptionallyBlueStudios',)).start()
        return "Check your browser for the github page."

    def openCheatSpy(self):
        threading.Thread(target=webbrowser.open_new_tab, args=('https://github.com/CheatSpy',)).start()
        return "Check your browser for the github page."

    def installCheatSpy(self):
        def do_install():
            try:
                print("Installing CheatSpy")
                print(f"Downloading script from {script_url}...")
                urllib.request.urlretrieve(script_url, temp_script_path)
                print(f"Script saved to {temp_script_path}")
                print("Executing Script")
                subprocess.run([sys.executable, temp_script_path])
            except Exception as e:
                print(f"Failed to install CheatSpy: {e}")
        threading.Thread(target=do_install).start()

    def openCheatSpyApp(self):
        def do_open():
            try:
                home_dir = os.path.expanduser("~")
                csins_dir = os.path.join(home_dir, "CheatSpyInstaller")
                csapp_dir = os.path.join(csins_dir, "CheatSpy-App")
                pythonfile_dir = os.path.join(csapp_dir, "gui.pyw")
                if os.path.exists(pythonfile_dir):
                    subprocess.run([sys.executable, pythonfile_dir])
                else:
                    print(f"CheatSpy App not found at {pythonfile_dir}")
            except Exception as e:
                print(f"Failed to open CheatSpy App: {e}")
        threading.Thread(target=do_open).start()

if __name__ == '__main__':
    api = API()
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()

    webview.create_window(
        title="BlueHub",
        url="https://optionallybluestudios.github.io/BlueHub?page=home&bhver=2",
        js_api=api,
        width=screen_width,
        height=screen_height,
        resizable=True,
        maximized=True,
    )

    webview.start(set_icon, gui='edgechromium')
