import customtkinter as ctk

# window
window = ctk.CTk()
window.title("CheatHub 0.1")
window.geometry("800x600")

# widgets

label = ctk.CTkLabel(window, text = 'Welcome to Cheathub')
label.pack()

# run
window.mainloop()