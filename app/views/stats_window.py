import tkinter as tk
from tkinter import ttk

from app.models.settings_model import SettingsModel

class DictViewerDialog(tk.Toplevel):
    def __init__(self, parent, data: dict[str, int]):
        super().__init__(parent)
        self.settings_model = SettingsModel()
        self.title(f"Results Viewer: {len(data)} words")
        self.geometry(f"{self.settings_model.settings.stats_window_width}x{self.settings_model.settings.stats_window_hieght}")
        self.minsize(200, 120)
        self.transient(parent)
        self.grab_set() # make modal

        self.protocol("WM_DELETE_WINDOW", self.on_window_delete)
        self.bind('<Escape>', lambda e: self.on_window_delete())

        self.data = data
        self.sorted_by = None
        self.sort_reverse = False

        frame = ttk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            frame,
            columns=("word", "count"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        self.tree.heading("word", text="Word", command=lambda: self.sort_column("word"))
        self.tree.heading("count", text="Count", command=lambda: self.sort_column("count"))
        self.tree.column("word", width=200, anchor="w")
        self.tree.column("count", width=50, anchor="e")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.tree.yview)

        self.populate()


    def populate(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert dictionary data into Treeview
        for word, count in self.data.items():
            self.tree.insert("", "end", values=(word, count))

        column: str = self.settings_model.settings.sort_order_in_stats
        if column == "count":
            # Sort by count in reverse order
            self.sort_column("count")
            self.sort_column("count")
        else:
            self.sort_column("word")


    def sort_column(self, column):
        # Extract data from tree
        items = [(self.tree.set(k, "word"), int(self.tree.set(k, "count")), k)
                 for k in self.tree.get_children()]

        # Determine sort key
        if column == "word":
            index = 0
        elif column == "count":
            index = 1
        else:
            return

        # Toggle sort order if same column is clicked
        if self.sorted_by == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
        self.sorted_by = column

        # Sort items and reinsert
        items.sort(key=lambda x: x[index], reverse=self.sort_reverse)

        for idx, (_, _, k) in enumerate(items):
            self.tree.move(k, '', idx)


    def on_window_delete(self):
        if self.settings_model.settings.remember_sort_order_in_stats:
            self.settings_model.settings.sort_order_in_stats = self.sorted_by
        if self.settings_model.settings.remember_windows_size:
            self.settings_model.settings.stats_window_width = self.winfo_width()
            self.settings_model.settings.stats_window_hieght = self.winfo_height()
        self.destroy()
