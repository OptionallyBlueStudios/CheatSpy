import customtkinter as ctk
import webbrowser

# window
window = ctk.CTk()
window.title("CheatHub v0-ALPHA")
window.geometry("800x600")

CreditsPage = ctk.CTk()
CreditsPage.title("Credits")
CreditsPage.geometry("300x400")

# widgets
label = ctk.CTkLabel(window, text='Welcome to CheatHub Alpha')
label.pack()

def button_event():
    webbrowser.open('https://cheatspy.short.gy/gh-reffrom-chub')

button = ctk.CTkButton(window, text="View Repository", command=button_event)
button.pack()

def OpenCredits():
    CreditsPage.mainloop()


credits = ctk.CTkButton(window, text='Open credits', command=OpenCredits)
credits.pack(side="bottom", pady=10) # Change Alignment To Bottom

# NOTE: You should probably use classes

# main loop
window.mainloop()

#  THINGS TO DO
# Use classes
# Style GUI
# Move Python Script To Folder
# Style orange
# Make fullscreenable (windowed)
#
#
#
#
#
#
#
#