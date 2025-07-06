# Import modules
import webbrowser
import subprocess
import sys
import platform

try:
    import customtkinter as ctk
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    import customtkinter as ctk

###### SETUP VARIABLES ######

window = ctk.CTk()
loginwind = ctk.CTk()
CreditsPage = ctk.CTk()
current_os = platform.system()
screen_width = window.winfo_screenwidth() - 300
screen_height = window.winfo_screenheight() - 300

###### SETUP WINDOWS ######

window.title("CheatHub v0-ALPHA")
window.geometry(f"{screen_width}x{screen_height}+0+0")

# Launch As Maximised
if current_os == "Windows":
    window.state('zoomed')
elif current_os == "Darwin":
    window.attributes('-zoomed', True)
else:
    window.attributes('-zoomed', True)

# Credits Window
CreditsPage.title("Credits")
CreditsPage.geometry("400x400")
# Login Window
loginwind.title("CheatHub | Login")
loginwind.geometry("300x300")

###### MAIN WINDOW ######

# Setup Functions
def button_event():
    webbrowser.open('https://cheatspy.short.gy/gh-reffrom-chub')

def OpenCredits():
    CreditsPage.mainloop()

# Setup Widgets
windowTitleMainTop = ctk.CTkLabel(window, text='Welcome to CheatHub Alpha')
windowTitleMainTop.pack()
viewRepoButton = ctk.CTkButton(window, text="View Repository", command=button_event)
viewRepoButton.pack()
creditsButton = ctk.CTkButton(window, text='Open credits', command=OpenCredits)
creditsButton.pack(side="bottom", pady=10) # Change Alignment To Bottom

###### CREDITS WINDOW ######

CreditsLabel = ctk.CTkLabel(CreditsPage, text="""Cheatspy And Cheathub made by OptionallyBlueStudios\n CheatSpy is a fork of nikos-pap's MemSpy\n All packages used in this are in the requirements.txt file""")
CreditsLabel.pack(expand=True)

# main loop
window.mainloop()

#  THINGS TO DO
# Use classes
# Style GUI
# Move Python Script To Folder
# Style orange
# Make fullscreenable (windowed) _/
# Add icon from Prtototoesypes.pyw
#
#
#
#
#
#
#