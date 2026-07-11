import os

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

from app.models.settings_model import SettingsModel

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.settings_model = SettingsModel()
        self.title("Settings")
        self.geometry(f"{self.settings_model.settings.settings_window_width}x{self.settings_model.settings.settings_window_hieght}")
        self.minsize(450, 250)
        self.resizable(True, True)
        self.transient(parent)
        self.grab_set()  # make modal

        self.protocol("WM_DELETE_WINDOW", self.on_window_delete)
        self.bind('<Escape>', lambda e: self.on_cancel())

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.setup_ui()
        # self.read_settings()


    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        self.create_scrollable_area(main_frame)
        self.create_bottom_panel(main_frame)


    def create_scrollable_area(self, parent):
        scroll_frame = ttk.Frame(parent)
        scroll_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        scroll_frame.columnconfigure(0, weight=1)
        scroll_frame.rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(scroll_frame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(scroll_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.bind_mousewheel_events()

        self.add_settings_sections()


    def create_bottom_panel(self, parent):
        bottom_frame = ttk.Frame(parent)
        bottom_frame.grid(row=1, column=0, sticky="ew", pady=(0, 0))
        bottom_frame.columnconfigure(1, weight=1)

        self.var_auto_save = tk.BooleanVar(value=self.settings_model.settings.persistent)
        auto_save_cb = ttk.Checkbutton(
            bottom_frame,
            text="Auto-save",
            variable=self.var_auto_save
        )
        auto_save_cb.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)

        button_frame = ttk.Frame(bottom_frame)
        button_frame.grid(row=0, column=1, sticky="e", pady=5)

        self.button_cancel = ttk.Button(button_frame, text="Cancel", command=self.on_cancel)
        self.button_cancel.grid(row=0, column=0, padx=(0, 5))

        self.button_reset = ttk.Button(button_frame, text="Reset", command=self.on_reset)
        self.button_reset.grid(row=0, column=1, padx=(0, 5))

        self.button_save_to_file = ttk.Button(button_frame, text="Save", command=self.on_save_to_file)
        self.button_save_to_file.grid(row=0, column=2, padx=(0, 5))

        self.button_apply = ttk.Button(button_frame, text="Apply", command=self.on_apply)
        self.button_apply.grid(row=0, column=3)


    def add_settings_sections(self):
        self.add_files_section()
        self.add_ui_section()


    def add_files_section(self):
        section = self.create_section("Files")

        # Open files from directory
        self.var_file_open_directory_enabled = tk.BooleanVar(value=self.settings_model.settings.file_open_directory_enabled)
        file_open_directory_enabled_checkbutton = ttk.Checkbutton(
            section,
            text="Default working directory:",
            variable=self.var_file_open_directory_enabled,
            command=self.toggle_open_directory_frame_state,
        )
        file_open_directory_enabled_checkbutton.pack(anchor="w", pady=2)

        file_open_directory_frame = ttk.Frame(section)
        file_open_directory_frame.pack(fill=tk.X, pady=2)

        self.file_open_directory_button = ttk.Button(file_open_directory_frame, text="Select...", command=self.on_select_open_directory)
        self.file_open_directory_button.pack(side="left", padx=(5, 0))

        self.var_file_open_directory = tk.StringVar(value=self.settings_model.settings.file_open_directory)
        self.file_open_directory_label = ttk.Label(file_open_directory_frame, textvariable=self.var_file_open_directory)
        self.file_open_directory_label.pack(side="left", padx=(5, 0))
        self.toggle_open_directory_frame_state()

        # Exclude words from file
        self.var_file_exclude_words_from_file_enabled = tk.BooleanVar(value=self.settings_model.settings.file_exclude_words_from_file_enabled)
        file_exclude_words_from_file_enabled_checkbutton = ttk.Checkbutton(
            section,
            text="Automatically add exclude file:",
            variable=self.var_file_exclude_words_from_file_enabled,
            command=self.toggle_file_exclude_words_from_file_frame_state,
        )
        file_exclude_words_from_file_enabled_checkbutton.pack(anchor="w", pady=2)

        file_exclude_words_from_file_frame = ttk.Frame(section)
        file_exclude_words_from_file_frame.pack(fill=tk.X, pady=2)

        self.file_exclude_words_from_file_button = ttk.Button(file_exclude_words_from_file_frame, text="Select...", command=self.on_select_exclude_file)
        self.file_exclude_words_from_file_button.pack(side="left", padx=(5, 0))

        self.var_file_exclude_words_from_file_filename = tk.StringVar()
        self.var_file_exclude_words_from_file = tk.StringVar()
        self.var_file_exclude_words_from_file.trace_add('write', lambda var, index, mode: self.var_file_exclude_words_from_file_filename.set(os.path.basename(self.var_file_exclude_words_from_file.get())))
        self.var_file_exclude_words_from_file.set(self.settings_model.settings.file_exclude_words_from_file)
        self.file_exclude_words_from_file_label = ttk.Label(file_exclude_words_from_file_frame, textvariable=self.var_file_exclude_words_from_file_filename)
        self.file_exclude_words_from_file_label.pack(side="left", padx=(5, 0))
        self.toggle_file_exclude_words_from_file_frame_state()

        # File size limit
        self.var_file_size_limit_enabled = tk.BooleanVar(value=self.settings_model.settings.file_size_limit_enabled)
        file_limit_checkbutton = ttk.Checkbutton(
            section,
            text="Enable file size limit",
            variable=self.var_file_size_limit_enabled,
            command=self.toggle_file_max_size_frame_state
        )
        file_limit_checkbutton.pack(anchor="w", pady=2)

        file_max_size_frame = ttk.Frame(section)
        file_max_size_frame.pack(fill=tk.X, pady=2)

        self.file_max_size_label = ttk.Label(file_max_size_frame, text="Max file size (Mb):")
        self.file_max_size_label.pack(side="left")

        self.var_file_max_size = tk.IntVar(value=self.settings_model.settings.file_max_size // 1024 // 1024)
        self.file_max_size_spinbox = ttk.Spinbox(
            file_max_size_frame,
            from_=1,
            to=100,
            textvariable=self.var_file_max_size,
            width=10,
            increment=1
        )
        self.file_max_size_spinbox.pack(side="right", padx=(5, 0))

        # File text encoding
        text_encoding_frame = ttk.Frame(section)
        text_encoding_frame.pack(fill=tk.X, pady=2)

        ttk.Label(text_encoding_frame, text="Fallback text encoding:").pack(side="left")

        self.var_fallback_file_text_encoding = tk.StringVar(value=self.settings_model.settings.fallback_file_text_encoding)
        self.text_encoding_combobox = ttk.Combobox(
            text_encoding_frame,
            textvariable=self.var_fallback_file_text_encoding,
            # state='readonly',
            values=["utf-8", "utf-16", "latin-1", "cp1252", "cp1251", "cp1125"]
        )
        self.text_encoding_combobox.pack(side="right", padx=(5, 0))

        # Additional file pattern
        file_additional_pattern_frame = ttk.Frame(section)
        file_additional_pattern_frame.pack(fill=tk.X, pady=2)

        ttk.Label(file_additional_pattern_frame, text="Additional file filter (e.g. *.ext):").pack(side="left")

        self.var_file_additional_pattern = tk.StringVar(value=self.settings_model.settings.file_additional_pattern)
        file_additional_pattern_entry = ttk.Entry(file_additional_pattern_frame, textvariable=self.var_file_additional_pattern)
        file_additional_pattern_entry.pack(side="right", padx=(5, 0))

        # Directories

        directory_files_pattern_frame = ttk.Frame(section)
        directory_files_pattern_frame.pack(fill=tk.X, pady=2)

        ttk.Label(directory_files_pattern_frame, text="Directory files filter:").pack(side="left")

        self.var_directory_files_pattern = tk.StringVar(value=self.settings_model.settings.directory_files_pattern)
        directory_files_pattern_entry = ttk.Entry(directory_files_pattern_frame, textvariable=self.var_directory_files_pattern)
        directory_files_pattern_entry.pack(side="right", padx=(5, 0))

        self.var_directory_recurcive_search = tk.BooleanVar(value=self.settings_model.settings.directory_recurcive_search)
        ttk.Checkbutton(
            section,
            text="Search recursively in directories",
            variable=self.var_directory_recurcive_search
        ).pack(anchor="w", pady=2)

        # Directory search file limit
        self.var_directory_files_limit_enabled = tk.BooleanVar(value=self.settings_model.settings.directory_files_limit_enabled)
        ttk.Checkbutton(
            section,
            text="Enable directories search file limit",
            variable=self.var_directory_files_limit_enabled,
            command=self.toggle_enable_directory_search_limit_state,
        ).pack(anchor="w", pady=2)

        directory_files_limit_frame = ttk.Frame(section)
        directory_files_limit_frame.pack(fill=tk.X, pady=2)

        self.directory_files_limit_label = ttk.Label(directory_files_limit_frame, text="Directories search file limit:")
        self.directory_files_limit_label.pack(side="left")

        self.var_directory_files_limit = tk.IntVar(value=self.settings_model.settings.directory_files_limit)
        self.directory_files_limit_spinbox = ttk.Spinbox(
            directory_files_limit_frame,
            from_=1,
            to=1000,
            textvariable=self.var_directory_files_limit,
            width=10,
            increment=1
        )
        self.directory_files_limit_spinbox.pack(side="right", padx=(5, 0))
        self.toggle_enable_directory_search_limit_state()


    def add_ui_section(self):
        section = self.create_section("Interface")

        theme_frame = ttk.Frame(section)
        theme_frame.pack(fill=tk.X, pady=2)

        ttk.Label(theme_frame, text="Theme:").pack(side="left")

        self.var_theme_name = tk.StringVar(value=self.settings_model.settings.theme_name)
        self.theme_name_combobox = ttk.Combobox(
            theme_frame,
            textvariable=self.var_theme_name,
            state='readonly',
            values=ttk.Style().theme_names()
        )
        self.theme_name_combobox.bind('<<ComboboxSelected>>', self.theme_changed)
        self.theme_name_combobox.pack(side="right", padx=(5, 0))

        self.var_remember_windows_size = tk.BooleanVar(value=self.settings_model.settings.remember_windows_size)
        ttk.Checkbutton(
            section,
            text="Remember windows size",
            variable=self.var_remember_windows_size
        ).pack(anchor="w", pady=2)

        self.var_remember_sort_order_in_stats = tk.BooleanVar(value=self.settings_model.settings.remember_sort_order_in_stats)
        ttk.Checkbutton(
            section,
            text="Remember order in Stats",
            variable=self.var_remember_sort_order_in_stats
        ).pack(anchor="w", pady=2)

        editor_font_frame = ttk.Frame(section)
        editor_font_frame.pack(fill=tk.X, pady=2)

        ttk.Label(editor_font_frame, text="Editor font size:").pack(side="left")

        self.var_editor_font_size = tk.IntVar(value=self.settings_model.settings.editor_font_size)
        ttk.Spinbox(
            editor_font_frame,
            from_=5,
            to=36,
            textvariable=self.var_editor_font_size,
            width=10
        ).pack(side="right", padx=(5, 0))


    def create_section(self, title):
        section_frame = ttk.LabelFrame(
            self.scrollable_frame,
            text=title,
            padding="10"
        )
        section_frame.pack(fill=tk.X, padx=5, pady=5)
        return section_frame


    def theme_changed(self, event):
        ttk.Style().theme_use(self.var_theme_name.get())


    def on_select_open_directory(self):
        selected_dir = filedialog.askdirectory(parent=self, title="Select Directory")
        if selected_dir:
            self.var_file_open_directory.set(selected_dir)


    def on_select_exclude_file(self):
        exclude_file_path = filedialog.askopenfilename(
            parent=self,
            title="Select files to add to exclude",
            filetypes=[("Supported files", "*.txt *.srt"), ("All files", "*.*")]
        )
        if exclude_file_path:
            self.var_file_exclude_words_from_file.set(exclude_file_path)


    def toggle_open_directory_frame_state(self):
        if self.var_file_open_directory_enabled.get():
            self.file_open_directory_button.config(state="normal")
            self.file_open_directory_label.config(state="normal")
        else:
            self.file_open_directory_button.config(state="disabled")
            self.file_open_directory_label.config(state="disabled")


    def toggle_file_exclude_words_from_file_frame_state(self):
        if self.var_file_exclude_words_from_file_enabled.get():
            self.file_exclude_words_from_file_button.config(state="normal")
            self.file_exclude_words_from_file_label.config(state="normal")
        else:
            self.file_exclude_words_from_file_button.config(state="disabled")
            self.file_exclude_words_from_file_label.config(state="disabled")


    def toggle_file_max_size_frame_state(self):
        if self.var_file_size_limit_enabled.get():
            self.file_max_size_spinbox.config(state="normal")
            self.file_max_size_label.config(state="normal")
        else:
            self.file_max_size_spinbox.config(state="disabled")
            self.file_max_size_label.config(state="disabled")


    def toggle_enable_directory_search_limit_state(self):
        if self.var_directory_files_limit_enabled.get():
            self.directory_files_limit_spinbox.config(state="normal")
            self.directory_files_limit_label.config(state="normal")
        else:
            self.directory_files_limit_spinbox.config(state="disabled")
            self.directory_files_limit_label.config(state="disabled")


    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)


    def bind_to_mousewheel(self, event):
            self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
            self.canvas.bind_all("<Button-4>", self.on_mousewheel)
            self.canvas.bind_all("<Button-5>", self.on_mousewheel)

    def unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def bind_mousewheel_events(self):
        self.canvas.bind('<Enter>', self.bind_to_mousewheel)
        self.canvas.bind('<Leave>', self.unbind_from_mousewheel)


    def on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")


    def read_settings(self):
        settings = self.settings_model.settings

        self.var_auto_save.set(settings.persistent)

        self.var_file_open_directory_enabled.set(settings.file_open_directory_enabled)
        self.var_file_open_directory.set(settings.file_open_directory)
        self.var_file_exclude_words_from_file_enabled.set(settings.file_exclude_words_from_file_enabled)
        self.var_file_exclude_words_from_file.set(settings.file_exclude_words_from_file)
        self.var_file_size_limit_enabled.set(settings.file_size_limit_enabled)
        self.var_file_max_size.set(settings.file_max_size // 1024 // 1024)
        self.var_fallback_file_text_encoding.set(settings.fallback_file_text_encoding)
        self.var_file_additional_pattern.set(settings.file_additional_pattern)

        self.var_directory_files_pattern.set(settings.directory_files_pattern)
        self.var_directory_recurcive_search.set(settings.directory_recurcive_search)
        self.var_directory_files_limit_enabled.set(settings.directory_files_limit_enabled)
        self.var_directory_files_limit.set(settings.directory_files_limit)

        self.var_theme_name.set(settings.theme_name)
        self.var_remember_windows_size.set(settings.remember_windows_size)
        self.var_remember_sort_order_in_stats.set(settings.remember_sort_order_in_stats)
        self.var_editor_font_size.set(settings.editor_font_size)

        self.toggle_open_directory_frame_state()
        self.toggle_file_exclude_words_from_file_frame_state()
        self.toggle_file_max_size_frame_state()
        self.toggle_enable_directory_search_limit_state()


    def save_settings(self):
        settings = self.settings_model.settings

        settings.persistent = self.var_auto_save.get()

        settings.file_open_directory_enabled = self.var_file_open_directory_enabled.get()
        settings.file_open_directory = self.var_file_open_directory.get()
        settings.file_exclude_words_from_file_enabled = self.var_file_exclude_words_from_file_enabled.get()
        settings.file_exclude_words_from_file = self.var_file_exclude_words_from_file.get()
        settings.file_size_limit_enabled = self.var_file_size_limit_enabled.get()
        settings.file_max_size = self.var_file_max_size.get() * 1024 * 1024
        settings.fallback_file_text_encoding = self.var_fallback_file_text_encoding.get()
        settings.file_additional_pattern = self.var_file_additional_pattern.get()

        settings.directory_files_pattern = self.var_directory_files_pattern.get()
        settings.directory_recurcive_search = self.var_directory_recurcive_search.get()
        settings.directory_files_limit_enabled = self.var_directory_files_limit_enabled.get()
        settings.directory_files_limit = self.var_directory_files_limit.get()

        settings.theme_name = self.var_theme_name.get()
        settings.remember_windows_size = self.var_remember_windows_size.get()
        settings.remember_sort_order_in_stats = self.var_remember_sort_order_in_stats.get()
        settings.editor_font_size = self.var_editor_font_size.get()


    def on_window_delete(self):
        self.unbind_from_mousewheel(None)
        if self.settings_model.settings.remember_windows_size:
            self.settings_model.settings.settings_window_width = self.winfo_width()
            self.settings_model.settings.settings_window_hieght = self.winfo_height()
        self.destroy()


    def on_cancel(self):
        # Reset theme just in case in was changed
        ttk.Style().theme_use(self.settings_model.settings.theme_name)
        self.on_window_delete()


    def on_reset(self):
        self.settings_model.reset_settings()
        self.read_settings()


    def on_save_to_file(self):
        self.save_settings()
        try:
            self.settings_model.save_to_file()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings into file: {e}", parent=self)
        self.on_apply()


    def on_apply(self):
        self.save_settings()
        self.on_window_delete()
