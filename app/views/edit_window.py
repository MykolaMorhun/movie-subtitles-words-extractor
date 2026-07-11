import tkinter as tk
from tkinter import ttk

from app.models.settings_model import SettingsModel

class EditResultWindow(tk.Toplevel):
    def __init__(self, parent, text=""):
        super().__init__(parent)
        self.settings_model = SettingsModel()
        self.title("Results Editor")
        self.geometry(f"{self.settings_model.settings.edit_window_width}x{self.settings_model.settings.edit_window_hieght}")
        self.minsize(200, 120)
        self.transient(parent)
        self.grab_set()  # make modal

        self.protocol("WM_DELETE_WINDOW", self.on_window_delete)
        self.bind('<Escape>', lambda e: self.on_window_delete())

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Frame for text and scrollbar
        text_frame = ttk.Frame(self)
        text_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.text_area = tk.Text(text_frame, wrap="word", font=(None, self.settings_model.settings.editor_font_size))
        self.text_area.insert("1.0", text)
        self.text_area.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_area.config(yscrollcommand=scrollbar.set)

        # Buttons panel
        button_frame = ttk.Frame(self)
        button_frame.grid(row=1, column=0, pady=10, sticky="ew")
        button_frame.columnconfigure((0, 1, 2), weight=1)

        save_to_file_button = ttk.Button(button_frame, text="Save to file", command=self.save_to_file)
        save_to_file_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(5, 5))

        copy_to_clipboard_button = ttk.Button(button_frame, text="Copy to clipboard", command=self.copy_to_clipboard)
        copy_to_clipboard_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))

        close_button = ttk.Button(button_frame, text="Close", command=self.on_window_delete)
        close_button.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(5, 5))


    def save_to_file(self):
        filepath = tk.filedialog.asksaveasfilename(
            parent=self,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return
        try:
            text = self.text_area.get("1.0", "end-1c")
            with open(filepath, 'w') as file:
                file.write(text)
        except Exception as e:
            tk.messagebox.showerror("Failed to save file", f"Failed to save into '{filepath}', reason: {str(e)}", parent=self)


    def copy_to_clipboard(self):
        text = self.text_area.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # Keeps clipboard even after window closes


    def on_window_delete(self):
        if self.settings_model.settings.remember_windows_size:
            self.settings_model.settings.edit_window_width = self.winfo_width()
            self.settings_model.settings.edit_window_hieght = self.winfo_height()
        self.destroy()