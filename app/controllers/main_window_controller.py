import os

from app.backend.words_manager import WordsManager

from app.models.main_window_model import MainWindowModel
from app.models.settings_model import SettingsModel
from app.views.edit_window import EditResultWindow
from app.views.stats_window import DictViewerDialog

class MainWindowController:
    def __init__(self, model: MainWindowModel, view):
        self.model: MainWindowModel = model
        self.view = view
        self.view.set_controller(self)

        self.settings_model = SettingsModel()

        # Subscribe main window model to the changes in the file list widgets models.
        self.view.files_include_model.add_observer(type('files_include_observer', (), {'update': lambda self, op, fr: model.files_include_update(op, fr)})())
        self.view.files_exclude_model.add_observer(type('files_exclude_model', (), {'update': lambda self, op, fr: model.files_exclude_update(op, fr)})())
        self.model.files_include_model = self.view.files_include_model
        self.model.files_exclude_model = self.view.files_exclude_model

        # Add default exclude file, if any
        if self.settings_model.settings.file_exclude_words_from_file_enabled and self.settings_model.settings.file_exclude_words_from_file:
            self.view.files_exclude_controller.add_item(self.settings_model.settings.file_exclude_words_from_file)

        # Change workdir according to settings
        if self.settings_model.settings.file_open_directory_enabled and self.settings_model.settings.file_open_directory:
            os.chdir(self.settings_model.settings.file_open_directory)


    def clear_all(self):
        self.view.files_include_controller.clear_items()
        self.view.files_exclude_controller.clear_items()
        self.model.reset()


    def save_file(self, filepath: str, data: str):
        if not filepath:
            return
        try:
            with open(filepath, 'w') as file:
                file.write(data)
        except Exception as e:
            self.view.show_error_modal(f"Failed to save data into '{filepath}' file: {e}")
            return


    def get_words_manager(self) -> WordsManager | None:
        if self.view.files_include_model.get_item_count() < 1:
            self.view.show_info_modal("No input files", "Select at least one file to include for processing.")
            return

        words_manager: WordsManager | None = None
        try:
            words_manager = self.model.get_words_manager()
        except Exception as e:
            self.view.show_error_modal(str(e))
            # import traceback
            # print(traceback.format_exc())
        return words_manager


    def save_result(self):
        words_manager = self.get_words_manager()
        if words_manager:
            result: str = words_manager.get_words_string()
            if not result:
                self.view.show_info_modal("Congratulations", "No content to save")
                return
            result_file: str = self.view.show_save_result_file_dialog()
            self.save_file(result_file, result)


    def show_preview_window(self):
        words_manager = self.get_words_manager()
        if words_manager:
            text = words_manager.get_words_string()
            if not text:
                self.view.show_info_modal("Congratulations", "No words to show")
                return
            EditResultWindow(self.view.root, text)


    def show_stats_window(self):
        words_manager = self.get_words_manager()
        if words_manager:
            data = words_manager.get_words_dict()
            if len(data) == 0:
                self.view.show_info_modal("Congratulations", "No words to show")
                return
            DictViewerDialog(self.view.root, data)


    def on_exit(self):
        if self.settings_model.settings.remember_windows_size:
            self.settings_model.settings.main_window_width = self.view.root.winfo_width()
            self.settings_model.settings.main_window_hieght = self.view.root.winfo_height()
        if self.settings_model.dirty and self.settings_model.settings.persistent:
            try:
                self.settings_model.save_to_file()
            except Exception as e:
                self.view.show_error_modal(f"Failed to save settings into file: {e}")

        self.view.root.destroy()
