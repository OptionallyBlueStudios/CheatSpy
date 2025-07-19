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

def setIcon(window):
    if os.path.exists(ICON_PATH):
        try:
            window.iconbitmap(ICON_PATH)
        except Exception as e:
            print(f"Failed to set icon: {e}")

# Download icon before creating any windows
download_icon()

###### SETUP WINDOWS ######
window = ctk.CTk()
loginwind = ctk.CTkToplevel()
CreditsPage = ctk.CTkToplevel()

screen_width = window.winfo_screenwidth() - 300
screen_height = window.winfo_screenheight() - 300

window.title("CheatHub v0-ALPHA")
window.geometry(f"{screen_width}x{screen_height}+0+0")

# Launch maximized depending on OS
if current_os == "Windows":
    window.state('zoomed')
else:
    window.attributes('-zoomed', True)

setIcon(window)
setIcon(CreditsPage)
setIcon(loginwind)

# Credits Window setup
CreditsPage.title("Credits")
CreditsPage.geometry("400x400")
CreditsPage.withdraw()  # Hide initially

# Login Window setup
loginwind.title("CheatHub | Login")
loginwind.geometry("300x300")
loginwind.withdraw()  # Hide initially

###### BUTTON CREATION FUNCTION ######
def create_styled_button(parent, text, command, style_tag=None, **kwargs):
    if style_tag == "transparent":
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            fg_color="transparent",
            text_color="white",
            hover_color="#2f2f2f",
            corner_radius=kwargs.get("corner_radius", 0),
            border_width=kwargs.get("border_width", 0),
            font=kwargs.get("font", ctk.CTkFont(weight="bold"))
        )
    else:
        # Default CTkButton style
        btn = ctk.CTkButton(
            parent,
            text=text,
            command=command,
            font=kwargs.get("font", ctk.CTkFont(size=14))
        )
    return btn

###### TAB SYSTEM SETUP ######
tab_frame = ctk.CTkFrame(window, fg_color="transparent")
tab_frame.pack(fill="x", pady=5)

current_tab = ctk.StringVar(value="Launch")

# Non-clickable label "CHEATHUB" at top-left of tab bar
cheathub_label = ctk.CTkLabel(
    tab_frame,
    text="CHEATHUB",
    font=ctk.CTkFont(size=20, weight="bold")
)
cheathub_label.pack(side="left", padx=10)

tab_names = ["Launch", "Settings"]
tab_buttons = {}

def update_underline():
    btn = tab_buttons[current_tab.get()]
    x = btn.winfo_x()
    width = btn.winfo_width()
    underline.configure(width=width)
    underline.place(x=x, y=30)

def switch_tab(tab_name):
    current_tab.set(tab_name)
    tab_pages[tab_name].lift()  # Bring this tab frame to front
    update_underline()
    window.update_idletasks()  # Reduce flicker by processing redraw events

# Create tab buttons with transparent style
for name in tab_names:
    btn = create_styled_button(
        tab_frame,
        name,
        lambda n=name: switch_tab(n),
        style_tag="transparent"
    )
    btn.pack(side="left", padx=5, pady=(0, 0))
    tab_buttons[name] = btn

# Green underline bar below tabs
underline = ctk.CTkFrame(
    tab_frame,
    height=3,
    width=50,
    fg_color="green",
    corner_radius=1
)
underline.place(x=8, y=30)

# Create tab pages stacked under the tab bar
tab_pages = {
    "Launch": ctk.CTkFrame(window),
    "Settings": ctk.CTkFrame(window),
}
for frame in tab_pages.values():
    frame.place(x=0, y=60, relwidth=1, relheight=1)

# Sample tab content
ctk.CTkLabel(
    tab_pages["Launch"],
    text="Launch CheatSpy Here!",
    font=ctk.CTkFont(size=16)
).pack(pady=20)

# Show default tab on startup
switch_tab("Launch")

###### MAIN WINDOW BUTTONS ######
def button_event():
    webbrowser.open('https://cheatspy.short.gy/gh-reffrom-chub')

def OpenCredits():
    CreditsPage.deiconify()  # Show credits window

# "View Repository" button with default style inside Launch tab
viewRepoButton = create_styled_button(
    tab_pages["Settings"],
    "View Repository",
    button_event,
    font=ctk.CTkFont(size=18, weight="bold")
)
viewRepoButton.pack()

# "Open credits" button with default style on main window
creditsButton = create_styled_button(
    tab_pages["Settings"],
    "Open credits",
    OpenCredits,  # <-- your function here
)
creditsButton.pack(padx=5)

###### CREDITS WINDOW ######
CreditsLabel = ctk.CTkLabel(
    CreditsPage,
    text=(
        "CheatSpy and CheatHub made by OptionallyBlueStudios\n"
        "CheatSpy is a fork of nikos-pap's MemSpy\n"
        "All packages used in this are in the requirements.txt file"
    )
)
CreditsLabel.pack(expand=True)

###### MAIN LOOP ######
window.mainloop()