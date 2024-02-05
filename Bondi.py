import tkinter as tk
from tkinter import messagebox
import pygame
import json
import os

class BondiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bondi")
        self.root.attributes('-fullscreen', True) 

        pygame.init()
        pygame.joystick.init()  # Initialize the joystick module

        self.joysticks = []
        self.current_joystick_index = 0  # Index of the currently selected joystick

        self.categories = self.read_categories()
        self.games = self.read_games()

        self.dark_mode = True
        self.sidebar_width = 230

        self.sidebar = tk.Frame(self.root, width=self.sidebar_width, bg="#1e1e1e")
        self.sub_area = tk.Frame(self.root, bg="#1e1e1e")
        self.game_buttons_frame = tk.Frame(self.sub_area, bg="#1e1e1e")

        self.create_sidebar_buttons()

        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sub_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.game_buttons_frame.pack(fill=tk.BOTH, expand=True)

        self.divider = tk.Canvas(self.root, width=2, height=600, bg="#333")
        self.divider.pack(side=tk.LEFT)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def read_categories(self):
        try:
            with open("Config/subsections.json") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def read_games(self):
        try:
            with open("Config/Games.json") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def create_sidebar_buttons(self):
        for category in self.categories:
            button = tk.Button(self.sidebar, text=category, command=lambda cat=category: self.display_game_buttons(cat), bg="#333", fg="white", font=("Helvetica", 14))
            button.pack(fill=tk.X)

        self.init_joysticks()  # Initialize joysticks after creating sidebar buttons

    def init_joysticks(self):
        joystick_count = pygame.joystick.get_count()
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)

    def handle_joystick_navigation(self, event):
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:  # Change joystick on button press
                self.current_joystick_index = (self.current_joystick_index + 1) % len(self.joysticks)
                self.display_game_buttons(self.categories[0])  # Refresh the displayed buttons

    def display_game_buttons(self, category):
        for widget in self.game_buttons_frame.winfo_children():
            widget.destroy()

        category_games = self.games.get(category, [])

        for game in category_games:
            name = game["name"]
            command = game["command"]
            button = tk.Button(self.game_buttons_frame, text=name, command=lambda cmd=command: self.run_command(cmd), bg="#333", fg="white", font=("Helvetica", 16))
            button.pack(side=tk.TOP, anchor='w')

    def run_command(self, command):
        os.system(command)

    def on_close(self):
        quit_dialog = tk.Toplevel(self.root)
        quit_dialog.configure(bg="#1e1e1e")

        label = tk.Label(quit_dialog, text="Are you sure you want to leave mate?", bg="#1e1e1e", fg="white")
        label.pack(padx=20, pady=10)

        button_frame = tk.Frame(quit_dialog, bg="#1e1e1e")
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=self.root.destroy, bg="#333", fg="white", padx=10)
        yes_button.pack(side=tk.LEFT)

        no_button = tk.Button(button_frame, text="No", command=quit_dialog.destroy, bg="#333", fg="white", padx=10)
        no_button.pack(side=tk.RIGHT)

        quit_dialog.transient(self.root)
        quit_dialog.grab_set()
        self.root.wait_window(quit_dialog)

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

    def run(self):
        self.root.bind("<Key>", self.handle_key_press)  # Bind key press event
        pygame.event.set_allowed([pygame.JOYBUTTONDOWN, pygame.JOYHATMOTION])  # Allow specific joystick events
        pygame.joystick.get_init()  
        self.root.after(100, self.check_joystick_events)  # Check joystick events every 100 milliseconds
        self.root.mainloop()

    def handle_key_press(self, event):
        if event.char.lower() == 'q':
            self.root.destroy()

    def check_joystick_events(self):
        pygame.event.pump()  # Pump the event queue
        for event in pygame.event.get():
            self.handle_joystick_navigation(event)  # Handle joystick navigation
        self.root.after(100, self.check_joystick_events)  # Schedule the next check

if __name__ == "__main__":
    if not os.path.exists("LICENSE"):
        messagebox.showerror("Error", "LICENSE file not found. Cannot run the application without this. Please redownload or update.")
    else:
        app = BondiApp()
        app.run()
