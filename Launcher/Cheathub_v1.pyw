import customtkinter as ctk
import webbrowser

# window
window = ctk.CTk()
window.title("CheatHub")
window.geometry("800x600")

# widgets

label = ctk.CTkLabel(window, text = 'OptionallyBlueStudios CheatHub v1')
label.pack()

def button_event():
    webbrowser.open ('https://cheatspy.short.gy/gh-reffrom-chub')

button = ctk.CTkButton(window, text="View Repository", command=button_event)
button.pack()
# run
window.mainloop()