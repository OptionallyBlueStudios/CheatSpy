import customtkinter as ctk
import webbrowser

# window(s)
window = ctk.CTk()
window.title("CheatHub v0-Alpha.1")
window.geometry("800x600")

Credits_page = ctk.CTk()
Credits_page.title("credits")
Credits_page.geometry("400x400")

# widgets

label = ctk.CTkLabel(window, text = 'Welcome to CheatHub Alpha')
label.pack()

def button_event():
    webbrowser.open ('https://cheatspy.short.gy/gh-reffrom-chub')

button = ctk.CTkButton(window, text="View Repository", command=button_event)
button.pack()

def open_credits():
    Credits_page.mainloop()

credits = ctk.CTkButton(window, text = 'Credits', command=open_credits)
credits.pack()

# run
window.mainloop()