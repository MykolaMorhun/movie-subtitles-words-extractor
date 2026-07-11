import os
import fnmatch

from app.models.file_list_widget_model import FilesListModel, FileRecord, FileListOperation
from app.views.file_list_widget_view import FileListView

from app.models.settings_model import SettingsModel


class FileListController:
    def __init__(self, model, view):
        self.model: FilesListModel = model
        self.view: FileListView = view
        self.model.add_observer(self.view)
        self.view.set_controller(self)
        self.view.update(FileListOperation.CLEAR, None)
        self.settings_model = SettingsModel()

    def add_item(self, file_path: str):
        if file_path and file_path.strip():
            self.model.add_item(file_path.strip())

    def remove_item(self, index: int):
        self.model.remove_item(index)

    def clear_items(self):
        self.model.clear_items()

    def get_items(self) -> list[FileRecord]:
        return self.model.get_items()

    def get_item_count(self) -> int:
        return self.model.get_item_count()

    def get_file_paths(self) -> list[str]:
        """Return list of full file paths"""
        return self.model.get_file_paths()

    def get_file_names(self) -> list[str]:
        """Return list of just filenames"""
        return self.model.get_file_names()


    def get_file_type_filters(self) -> list[str]:
        """Returns list of filters to choose from in file select dialog"""
        filetypes = [
            ("Supported files", "*.txt *.srt"),
            ("Subtitles files", "*.srt"),
            ("Text files", "*.txt"),
            ("All files", "*.*"),
        ]
        if self.settings_model.settings.file_additional_pattern:
            filetypes.insert(len(filetypes) - 1, ("User defined", self.settings_model.settings.file_additional_pattern))
        return filetypes


    def add_files_from_directory(self, directory: str) -> bool:
        """
        Adds files from the directory according to the settings.
        Returns True if search was interrupted due to file number limit.
        """
        is_recurcive: bool = self.settings_model.settings.directory_recurcive_search

        files_limit: int = 0 # no limit
        if self.settings_model.settings.directory_files_limit_enabled:
            files_limit = self.settings_model.settings.directory_files_limit

        directory_files_pattern = self.settings_model.settings.directory_files_pattern
        if directory_files_pattern == "":
            directory_files_pattern = "*.srt *.txt"

        files, is_interrupted = self._search_files_in_directory(directory, directory_files_pattern, is_recurcive, files_limit)
        for f in files:
            self.add_item(f)

        return not is_interrupted


    def _search_files_in_directory(self, directory: str, pattern: str, recursive: bool, files_limit: int) -> tuple[list[str], bool]:
        """
        Searches in given directory for files, respecting search options:
          - pattern of file (e.g. "*.srt *.txt")
          - recursive: whether perform recursive search in subdirectories
          - files_limit: stops when found given number of files

        Returns list of found files and flag that is False when search was interrupted due to the limit.
        """

        patterns = pattern.split()

        files: list[str] = []
        files_found: int = 0

        def matches_patterns(filename: str) -> bool:
            for p in patterns:
                if fnmatch.fnmatch(filename, p):
                    return True
            return False

        for root, dirs, filenames in os.walk(directory):
            for filename in filenames:
                if matches_patterns(filename):
                    files.append(os.path.join(root, filename))
                    files_found += 1
                    if files_limit > 0 and files_found >= files_limit:
                        # Limit is reached
                        return files, False
            if not recursive:
                # Stop after processing top directory if recursive search is disabled
                break

        return files, True
