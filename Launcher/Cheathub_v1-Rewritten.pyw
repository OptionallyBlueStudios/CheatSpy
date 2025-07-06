# Import modules
import webbrowser
import subprocess
import sys
import platform
import os
import urllib.request

###### Download Missing Modules ######

try:
    import customtkinter as ctk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

###### SETUP VARIABLES ######

USER_HOME = os.path.expanduser("~")
ICON_URL = "https://raw.githubusercontent.com/OptionallyBlueStudios/CheatSpy/refs/heads/development/icon.ico"
ICON_PATH = os.path.join(USER_HOME, "CheatHubData", "icon.ico")
current_os = platform.system()

###### SETUP FUNCTIONS ######

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

def setIcon(windowNameType):
    if os.path.exists(ICON_PATH):
        try:
            windowNameType.iconbitmap(ICON_PATH)
        except Exception as e:
            print(f"Failed to set icon: {e}")

# --- DOWNLOAD ICON BEFORE ANY WINDOWS ---
download_icon()

###### SETUP WINDOWS ######

window = ctk.CTk()
loginwind = ctk.CTkToplevel()
CreditsPage = ctk.CTkToplevel()

screen_width = window.winfo_screenwidth() - 300
screen_height = window.winfo_screenheight() - 300

window.title("CheatHub v0-ALPHA")
window.geometry(f"{screen_width}x{screen_height}+0+0")

# Launch As Maximised
if current_os == "Windows":
    window.state('zoomed')
else:
    window.attributes('-zoomed', True)

setIcon(window)
setIcon(CreditsPage)
setIcon(loginwind)

# Credits Window
CreditsPage.title("Credits")
CreditsPage.geometry("400x400")
CreditsPage.withdraw()  # Hide at start

# Login Window
loginwind.title("CheatHub | Login")
loginwind.geometry("300x300")
loginwind.withdraw()  # Hide at start

###### MAIN WINDOW ######

# Setup Functions
def button_event():
    webbrowser.open('https://cheatspy.short.gy/gh-reffrom-chub')

def OpenCredits():
    CreditsPage.deiconify()  # Show window

# Setup Widgets
viewRepoButton = ctk.CTkButton(window, text="View Repository", command=button_event, font=ctk.CTkFont(size=18, weight="bold"), fg_color="transparent", text_color="white", hover=False)
viewRepoButton.pack(anchor="nw", padx=10, pady=10)
creditsButton = ctk.CTkButton(window, text='Open credits', command=OpenCredits)
creditsButton.pack(side="bottom", pady=10)

###### CREDITS WINDOW ######

CreditsLabel = ctk.CTkLabel(CreditsPage, text="""CheatSpy and CheatHub made by OptionallyBlueStudios\nCheatSpy is a fork of nikos-pap's MemSpy\nAll packages used in this are in the requirements.txt file""")
CreditsLabel.pack(expand=True)

# main loop
window.mainloop()