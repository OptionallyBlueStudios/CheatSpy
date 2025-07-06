import customtkinter as ctk
import webbrowser

# window
window = ctk.CTk()
window.title("CheatHub 0.1")
window.geometry("800x600")

# widgets

label = ctk.CTkLabel(window, text = 'Welcome to Cheathub')
label.pack()

def button_event():
    webbrowser.open ('https://github.com/OptionallyBlueStudios/CheatSpy')

button = ctk.CTkButton(window, text="github page", command=button_event)
button.pack()
# run
window.mainloop()