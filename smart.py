"""Home page for launching the animal comparison apps."""

import subprocess
import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox


APP_DIRECTORY = Path(__file__).resolve().parent
ANIMAL_APPS = {
    "Bird vs Chicken": "bird_chicken_app2.py",
    "Dog vs Cat": "dogcat_app.py",
}


def launch_app(script_name):
    script_path = APP_DIRECTORY / script_name
    if not script_path.is_file():
        messagebox.showerror(
            "App not found",
            f"Could not find {script_name} in:\n{APP_DIRECTORY}",
            parent=root,
        )
        return

    try:
        subprocess.Popen([sys.executable, str(script_path)], cwd=APP_DIRECTORY)
    except OSError as error:
        messagebox.showerror(
            "Could not launch app",
            f"Unable to start {script_name}:\n{error}",
            parent=root,
        )


root = tk.Tk()
root.title("Animal Comparisons")
root.geometry("480x360")
root.resizable(False, False)

menu_bar = tk.Menu(root)
apps_menu = tk.Menu(menu_bar, tearoff=False)
for app_name, script_name in ANIMAL_APPS.items():
    apps_menu.add_command(
        label=app_name,
        command=lambda name=script_name: launch_app(name),
    )
menu_bar.add_cascade(label="Compare", menu=apps_menu)
root.config(menu=menu_bar)

tk.Label(
    root,
    text="Animal Comparisons",
    font=("Segoe UI", 22, "bold"),
).pack(pady=(30, 8))

tk.Label(
    root,
    text="Choose an animal pair to compare an image.",
    font=("Segoe UI", 11),
).pack(pady=(0, 24))

for app_name, script_name in ANIMAL_APPS.items():
    tk.Button(
        root,
        text=app_name,
        command=lambda name=script_name: launch_app(name),
        font=("Segoe UI", 12),
        width=25,
        padx=12,
        pady=8,
    ).pack(pady=8)

root.mainloop()