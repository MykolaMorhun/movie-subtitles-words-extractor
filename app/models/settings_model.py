import os
import configparser

from tkinter import ttk # for default theme detection

MAX_FILE_SIZE = 5 * 1024 * 1024

class Settings:
    def __init__(self, change_settings_callback):
        self._notify = False
        self.reset_settings()
        self._change_settings_callback = change_settings_callback
        self._notify = True

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == "_notify":
            return
        if self._notify:
            old_value = getattr(self, name, None)
            if old_value != value:
                self._change_settings_callback(name, value)


    def reset_settings(self):
        # Auto save of settings on each exit
        self.persistent: bool = False

        self.file_open_directory_enabled: bool = False
        self.file_open_directory: str = "" # Empty means current directory
        self.file_exclude_words_from_file_enabled: bool = False
        self.file_exclude_words_from_file: str = ""
        self.file_size_limit_enabled: bool = True
        self.file_max_size: int = MAX_FILE_SIZE
        self.fallback_file_text_encoding: str = "utf-8"
        self.file_additional_pattern = "" # "*.srt *.txt"

        self.directory_files_pattern: str = "*.srt *.txt"
        self.directory_recurcive_search: bool = False
        self.directory_files_limit_enabled: bool = True
        self.directory_files_limit: int = 100

        self.theme_name = self.get_default_theme_name()
        self.remember_windows_size: bool = True
        self.main_window_width: int = 500
        self.main_window_hieght: int = 450
        self.settings_window_width: int = 500
        self.settings_window_hieght: int = 550
        self.stats_window_width: int = 300
        self.stats_window_hieght: int = 400
        self.edit_window_width: int = 500
        self.edit_window_hieght: int = 500

        self.remember_sort_order_in_stats: bool = True
        self.sort_order_in_stats: str = ""

        self.editor_font_size: int = 12

    def get_default_theme_name(self) -> str:
        # Instead of using default tk theme, try to use OS specific theme.
        themes = ttk.Style().theme_names()
        if 'winnative' in themes:
            return 'winnative'
        elif 'aqua' in themes:
            return 'aqua'
        return 'default'


class SettingsModel:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsModel, cls).__new__(cls)
            cls._instance._config = configparser.ConfigParser()
            cls._instance._file_path = "spsettings.ini"
            cls._instance._observers = []
            cls._instance.settings = Settings(cls._instance.notify_observers)
            cls._instance.load_from_file(cls._instance._file_path)
            cls._instance.dirty = False
        return cls._instance

    def reset_settings(self):
        self.settings.reset_settings()


    def load_from_file(self, settings_file_path: str):
        if os.path.exists(settings_file_path) and os.path.isfile(settings_file_path):
            self._config.read(self._file_path)

            self.settings.persistent = self._config.getboolean("Settings", "persistent")

            self.settings.file_open_directory_enabled = self._config.getboolean("Files", "file_open_directory_enabled")
            self.settings.file_open_directory = self._config.get("Files", "file_open_directory")
            self.settings.file_exclude_words_from_file_enabled = self._config.getboolean("Files", "file_exclude_words_from_file_enabled")
            self.settings.file_exclude_words_from_file = self._config.get("Files", "file_exclude_words_from_file")
            self.settings.file_size_limit_enabled = self._config.getboolean("Files", "file_size_limit_enabled")
            self.settings.file_max_size = self._config.getint("Files", "file_max_size")
            self.settings.fallback_file_text_encoding = self._config.get("Files", "fallback_file_text_encoding")
            self.settings.files_additional_pattern = self._config.get("Files", "file_additional_pattern")

            self.settings.directory_files_pattern = self._config.get("Files", "directory_files_pattern")
            self.settings.directory_recurcive_search = self._config.getboolean("Files", "directory_recurcive_search")
            self.settings.directory_files_limit_enabled = self._config.getboolean("Files", "directory_files_limit_enabled")
            self.settings.directory_files_limit = self._config.getint("Files", "directory_files_limit")

            self.settings.theme_name             = self._config.get("UI", "theme_name")
            self.settings.remember_windows_size  = self._config.getboolean("UI", "remember_windows_size")
            self.settings.main_window_width      = self._config.getint("UI", "main_window_width")
            self.settings.main_window_hieght     = self._config.getint("UI", "main_window_hieght")
            self.settings.settings_window_width  = self._config.getint("UI", "settings_window_width")
            self.settings.settings_window_hieght = self._config.getint("UI", "settings_window_hieght")
            self.settings.stats_window_width     = self._config.getint("UI", "stats_window_width")
            self.settings.stats_window_hieght    = self._config.getint("UI", "stats_window_hieght")
            self.settings.edit_window_width      = self._config.getint("UI", "edit_window_width")
            self.settings.edit_window_hieght     = self._config.getint("UI", "edit_window_hieght")

            self.settings.remember_sort_order_in_stats = self._config.getboolean("UI", "remember_sort_order_in_stats")
            self.settings.sort_order_in_stats = self._config.get("UI", "sort_order_in_stats")

            self.settings.editor_font_size = self._config.getint("UI", "editor_font_size")


    def save_to_file(self, file_path: str | None = None):
        settings_file_path = file_path or self._file_path

        self._config["Settings"] = {
                "persistent": self.settings.persistent,
        }
        self._config["Files"] = {
                "file_open_directory_enabled": self.settings.file_open_directory_enabled,
                "file_open_directory": self.settings.file_open_directory,
                "file_exclude_words_from_file_enabled": self.settings.file_exclude_words_from_file_enabled,
                "file_exclude_words_from_file": self.settings.file_exclude_words_from_file,
                "file_size_limit_enabled": self.settings.file_size_limit_enabled,
                "file_max_size": self.settings.file_max_size,
                "fallback_file_text_encoding": self.settings.fallback_file_text_encoding,
                "file_additional_pattern": self.settings.file_additional_pattern,

                "directory_files_pattern": self.settings.directory_files_pattern,
                "directory_recurcive_search": self.settings.directory_recurcive_search,
                "directory_files_limit_enabled": self.settings.directory_files_limit_enabled,
                "directory_files_limit": self.settings.directory_files_limit,
        }
        self._config["UI"] = {
                "theme_name": self.settings.theme_name,

                "remember_windows_size": self.settings.remember_windows_size,
                "main_window_width": self.settings.main_window_width,
                "main_window_hieght": self.settings.main_window_hieght,
                "settings_window_width": self.settings.settings_window_width,
                "settings_window_hieght": self.settings.settings_window_hieght,
                "stats_window_width": self.settings.stats_window_width,
                "stats_window_hieght": self.settings.stats_window_hieght,
                "edit_window_width": self.settings.edit_window_width,
                "edit_window_hieght": self.settings.edit_window_hieght,

                "remember_sort_order_in_stats": self.settings.remember_sort_order_in_stats,
                "sort_order_in_stats": self.settings.sort_order_in_stats,

                "editor_font_size": self.settings.editor_font_size
        }
        with open(settings_file_path, "w") as configfile:
            self._config.write(configfile)


    def add_observer(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)


    def remove_observer(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)


    def notify_observers(self, name: str, value: any):
        self.dirty = True
        for observer in self._observers:
            observer.setting_change(name, value)
