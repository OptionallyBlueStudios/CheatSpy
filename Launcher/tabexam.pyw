import customtkinter as ctk

ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("500x400")
app.title("Minecraft Launcher Style Tabs")

# --- Tabs as buttons ---
tab_frame = ctk.CTkFrame(app, fg_color="transparent")
tab_frame.pack(fill="x", pady=5)

current_tab = ctk.StringVar(value="Home")

def switch_tab(tab_name):
    current_tab.set(tab_name)
    for frame in tab_pages.values():
        frame.pack_forget()
    tab_pages[tab_name].pack(fill="both", expand=True)

tab_names = ["Home", "Play", "Settings"]
tab_buttons = {}

for name in tab_names:
    btn = ctk.CTkButton(
        tab_frame,
        text=name,
        font=ctk.CTkFont(weight="bold"),
        fg_color="transparent",
        text_color=("gray80", "white"),
        hover_color="#2f2f2f",
        command=lambda n=name: switch_tab(n)
    )
    btn.pack(side="left", padx=5, pady=(0, 0))
    tab_buttons[name] = btn

# --- Green underline bar ---
underline = ctk.CTkFrame(tab_frame, height=3, width=50, fg_color="green", corner_radius=1)
underline.place(x=8, y=30)  # Initial position under "Home"

# --- Pages/frames for each tab ---
tab_pages = {
    "Home": ctk.CTkFrame(app),
    "Play": ctk.CTkFrame(app),
    "Settings": ctk.CTkFrame(app),
}

# Sample content
ctk.CTkLabel(tab_pages["Home"], text="Welcome to Home!").pack(pady=20)
ctk.CTkLabel(tab_pages["Play"], text="Play Minecraft!").pack(pady=20)
ctk.CTkLabel(tab_pages["Settings"], text="Launcher Settings").pack(pady=20)

# --- Update underline position when switching tabs ---
def update_underline():
    btn = tab_buttons[current_tab.get()]
    x = btn.winfo_x()
    width = btn.winfo_width()
    underline.place(x=x, y=30, width=width)

def on_tab_click(tab_name):
    switch_tab(tab_name)
    app.after(10, update_underline)  # Slight delay to allow widget sizes to update

# Reassign with underline updater
for name, btn in tab_buttons.items():
    btn.configure(command=lambda n=name: on_tab_click(n))

# Show default tab
switch_tab("Home")
app.after(10, update_underline)

app.mainloop()
