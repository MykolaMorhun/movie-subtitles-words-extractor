import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import webbrowser

from app.models.settings_model import SettingsModel
from app.models.file_list_widget_model import FilesListModel
from app.views.file_list_widget_view import FileListView
from app.controllers.file_list_widget_controller import FileListController
from app.controllers.main_window_controller import MainWindowController
from app.views.about_window import AboutDialog
from app.views.settings_window_view import SettingsWindow
from app.consts import ONLINE_DOC_URL

class MainWindowView:
    def __init__(self, root):
        self.root = root
        self.controller: MainWindowController | None = None
        self.settings_model = SettingsModel()
        ttk.Style().theme_use(self.settings_model.settings.theme_name)
        self.setup_ui()
        self.load_app_image()

    def set_controller(self, controller):
        self.controller = controller
        self.root.protocol("WM_DELETE_WINDOW", controller.on_exit)

    def load_app_image(self):
        try:
            logo_image = tk.PhotoImage(file=os.path.join(".", "images", "logo.png"))
            self.root.iconphoto(True, logo_image)
        except tk.TclError:
            try:
                logo_image = tk.PhotoImage(file=os.path.join(".", "images", "logo.ico"))
                self.root.iconphoto(True, logo_image)
            except tk.TclError:
                print("Warning: could not load app image.")

    def setup_ui(self):
        self.root.title("Movie Subtitles Words Extractor Application")
        self.root.geometry(f"{self.settings_model.settings.main_window_width}x{self.settings_model.settings.main_window_hieght}")
        self.root.minsize(400, 425)
        self.set_window_logo()

        self.setup_menu()

        main_frame = self.root
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.files_include_model = FilesListModel()
        self.files_include_view = FileListView(main_frame, "Include words from files", row_number=5)
        self.files_include_controller = FileListController(self.files_include_model, self.files_include_view)
        self.files_include_view.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 2))

        self.files_exclude_model = FilesListModel()
        self.files_exclude_view = FileListView(main_frame, "Exclude words from files", row_number=3)
        self.files_exclude_controller = FileListController(self.files_exclude_model, self.files_exclude_view)
        self.files_exclude_view.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 2))

        button_bar_frame = ttk.Frame(main_frame)
        button_bar_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky=(tk.W, tk.E))

        # Configure grid weights to make buttons expand
        button_bar_frame.columnconfigure(0, weight=1)
        button_bar_frame.columnconfigure(1, weight=1)
        button_bar_frame.columnconfigure(2, weight=1)
        button_bar_frame.columnconfigure(3, weight=1)

        self.run_and_save_button = ttk.Button(button_bar_frame, text="Process and Save", command=self.on_save)
        self.run_and_save_button.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(5, 5))

        self.preview_button = ttk.Button(button_bar_frame, text="Preview", command=self.on_preview)
        self.preview_button.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5))

        self.stats_button = ttk.Button(button_bar_frame, text="Stats", command=self.on_show_stats)
        self.stats_button.grid(row=0, column=2, sticky=(tk.W, tk.E), padx=(5, 5))

        self.clear_button = ttk.Button(button_bar_frame, text="Clear", command=self.on_clear)
        self.clear_button.grid(row=0, column=3, sticky=(tk.W, tk.E), padx=(5, 5))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=2)  # First FileListView gets 2/3 weight
        main_frame.rowconfigure(2, weight=1)  # Second FileListView gets 1/3 weight

    def set_window_logo(self):
        """Sets the window picture at runtime"""
        try:
            if getattr(sys, 'frozen', False):
                # Running as binary
                logo_path = os.path.join(os.path.dirname(sys.executable), 'logo.png')
                if not os.path.exists(logo_path):
                    logo_path = os.path.join(os.getcwd(), 'logo.png')
            else:
                # Running as script
                logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logo.png')

            if os.path.exists(logo_path):
                self.root.iconbitmap(logo_path)
        except:
            # failed to load the logo, proceed without i
            pass


    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        program_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Program", menu=program_menu)
        program_menu.add_command(label ='Settings', command = lambda: SettingsWindow(self.root))
        program_menu.add_command(label ='Exit', command = lambda: self.controller.on_exit())

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label ='About', command = lambda: AboutDialog(self.root))
        help_menu.add_command(label ='Online help', command = lambda: webbrowser.open_new_tab(ONLINE_DOC_URL))

    def on_save(self):
        if self.controller:
            self.controller.save_result()

    def on_preview(self):
        if self.controller:
            self.controller.show_preview_window()

    def on_show_stats(self):
        if self.controller:
            self.controller.show_stats_window()


    def on_clear(self):
        if self.controller:
            self.controller.clear_all()

    def get_include_files(self):
        return self.files_include_controller.get_items()

    def get_exclude_files(self):
        return self.files_exclude_controller.get_items()

    def show_info_modal(self, title, message: str):
        messagebox.showinfo(title, message)

    def show_error_modal(self, message: str):
        messagebox.showerror("Error", message)

    def show_save_result_file_dialog(self) -> str:
        return filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
