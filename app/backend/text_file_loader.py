import os

from app.models.settings_model import SettingsModel


class FileTooBigError(Exception):
    """Raised when file is too big to to loaded"""

    def __init__(self, file: str, file_size: int):
        self.message = f"File '{file}' has size {file_size / 1024 / 1024:.1f}Mb that exceeds allowed size."
        super().__init__(self.message)


class TextFileLoader:
    """
    Loads content of a text file into a list of strings
    where each item represents a line from the file.
    """

    def __init__(self, path: str):
        self.path = path
        self._settings_model = SettingsModel()

    @property
    def path(self) -> str | None :
        return self._path

    @path.setter
    def path(self, value: str) -> str:
        if len(value) == 0:
            raise ValueError("File path is empty.")
        self._path = value

    def load(self) -> str:
        """
        Reads a text file into a string if its size is less than settings.file_max_size.
        Returns the content of the file as a string if successful
        Raises:
          - FileTooBigError if file size exceeds settings.file_max_size.
          - ValueError if the file is not regular file, e.g. a directory.
          - FileNotFoundError
        """
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File '{self.path}' not found.")

        if not os.path.isfile(self.path):
            raise ValueError(f"File '{self.path}' is not regular file.")

        if self._settings_model.settings.file_size_limit_enabled:
            file_size = os.path.getsize(self.path)
            if file_size > self._settings_model.settings.file_max_size:
                raise FileTooBigError(self.path, file_size)

        # file_encoding = None # Use system default encoding
        # if not self._settings_model.settings.file_text_encoding.casefold() in {"default", "auto", "autodetect"}:
        #     file_encoding: str = self._settings_model.settings.file_text_encoding.casefold()
        # with open(self.path, 'r', encoding=file_encoding) as f:
        #         return f.read()

        try:
            with open(self.path, 'r') as f:
                return f.read()
        except UnicodeDecodeError:
            # System default encoding failed, try fallback encoding from the settings.
            file_encoding: str = self._settings_model.settings.fallback_file_text_encoding
            with open(self.path, 'r', encoding=file_encoding) as f:
                return f.read()
