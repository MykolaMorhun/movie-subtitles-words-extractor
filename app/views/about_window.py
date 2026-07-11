import tkinter as tk
from tkinter import ttk
import webbrowser

from app.consts import VERSION, HOMEPAGE_URL

class AboutDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("About Movie Subtitles Words Extractor")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set() # make modal

        # Padding around all content
        padding = {"padx": 10, "pady": 2}
        ttk.Label(self, text="Movie Subtitles Words Extractor").pack(**padding)
        ttk.Label(self, text="Version: " + VERSION).pack(**padding)
        ttk.Label(self, text="(c) 2026 Mykola Morhun").pack(**padding)
        # Create link to homepage
        link = tk.Label(self, text="Homepage", fg="blue", cursor="hand2")
        link.pack(**padding)
        link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(HOMEPAGE_URL))

        ok_button = ttk.Button(self, text="OK", command=self.destroy)
        ok_button.pack(pady=(10, 15))
        ok_button.focus()

        self.bind('<Escape>', lambda e: self.destroy())

        self.center_over_parent(parent)


    def center_over_parent(self, parent):
        parent.update_idletasks()

        pw = parent.winfo_width()
        ph = parent.winfo_height()
        px = parent.winfo_rootx()
        py = parent.winfo_rooty()

        w = self.winfo_width()
        h = self.winfo_height()

        x = px + (pw - w) // 2
        y = py + (ph - h) // 2

        self.geometry(f"+{x}+{y}")
