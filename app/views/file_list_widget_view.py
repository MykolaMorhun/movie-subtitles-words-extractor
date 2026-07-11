import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class FileListView:
    def __init__(self, parent, title="Files", row_number=5):
        self.parent = parent
        self.controller = None
        self.title = title
        self.rows = row_number
        self.setup_ui()

    def set_controller(self, controller):
        self.controller = controller

    def setup_ui(self):
        self.frame = ttk.LabelFrame(self.parent, text=self.title, padding="10")

        # Create listbox with scrollbar
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.listbox = tk.Listbox(list_frame, height=self.rows, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Button frame at the bottom
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X)

        self.add_files_button = ttk.Button(button_frame, text="Add Files", command=self.on_add_files)
        self.add_files_button.pack(side=tk.LEFT, padx=(0, 5))

        self.add_directory_button = ttk.Button(button_frame, text="Add Directory", command=self.on_add_directory)
        self.add_directory_button.pack(side=tk.LEFT, padx=(0, 5))

        self.remove_button = ttk.Button(button_frame, text="Remove File", command=self.on_remove_file)
        self.remove_button.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.on_clear_table)
        self.clear_button.pack(side=tk.LEFT)

    def on_add_files(self):
        self.show_file_dialog()

    def on_add_directory(self):
        self.show_directory_dialog()

    def on_remove_file(self):
        if self.controller:
            selection = self.listbox.curselection()
            for index in sorted(selection, reverse=True):
                self.controller.remove_item(index)

    def on_clear_table(self):
        if self.controller:
            self.controller.clear_items()


    def show_file_dialog(self):
        if not self.controller:
            return

        file_paths = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=self.controller.get_file_type_filters()
        )

        if file_paths and self.controller:
            for file_path in file_paths:
                self.controller.add_item(file_path)


    def show_directory_dialog(self):
        if not self.controller:
            return

        selected_dir = filedialog.askdirectory(title="Select Directory")
        if selected_dir:
            try:
                is_file_limit_reached: bool = self.controller.add_files_from_directory(selected_dir)
                if is_file_limit_reached:
                    tk.messagebox.showinfo("Warning", "Some files were ignored due to file limit settings")
            except Exception as e:
                tk.messagebox.showerror("Error", str(e))


    def update(self, operation, fileRecord):
        if self.controller:
            # Clear the whole list
            self.listbox.delete(0, tk.END)

            items = self.controller.get_items()
            for item in items:
                filename = os.path.basename(item.name)
                self.listbox.insert(tk.END, filename)


    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)