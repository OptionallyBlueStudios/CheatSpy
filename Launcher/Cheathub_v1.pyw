import customtkinter as ctk
import webbrowser

# window
window = ctk.CTk()
window.title("CheatHub v0-ALPHA")
window.geometry("800x600")

# widgets
label = ctk.CTkLabel(window, text='Welcome to CheatHub Alpha')
label.pack()

def button_event():
    webbrowser.open('https://cheatspy.short.gy/gh-reffrom-chub')

button = ctk.CTkButton(window, text="View Repository", command=button_event)
button.pack()

credits = ctk.CTkLabel(window, text='Made by OptionallyBlueStudios')
credits.pack(side="bottom") # Change Alignment To Bottom

# NOTE: You should probably use classes

# main loop
window.mainloop()