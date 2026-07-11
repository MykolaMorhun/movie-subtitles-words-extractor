from app.backend.text_file_loader import TextFileLoader
from app.backend.words_manager import WordsManager, WordsSource
from app.backend.subtitles_processor import create_words_counter

from app.models.file_list_widget_model import FilesListModel, FileListOperation, FileRecord

class MainWindowModel:
    def __init__(self):
        self.reset()
        self.files_include_model: FilesListModel | None = None
        self.files_exclude_model: FilesListModel | None = None

    def reset(self):
        self._words_manager: WordsManager | None = None
        self._dirty = True

    def files_include_update(self, operation: FileListOperation, fileRecord: FileRecord | None):
        self._dirty = True

    def files_exclude_update(self, operation: FileListOperation, fileRecord: FileRecord | None):
        self._dirty = True

    def get_words_manager(self) -> WordsManager:
        if self._dirty:
            include_files = self.files_include_model.get_items()
            if not include_files:
                return
            exclude_files = self.files_exclude_model.get_items()

            self._words_manager = WordsManager()
            for fr in include_files:
                try:
                    is_subtitles: bool = True if fr.name.lower().endswith(".srt") else False
                    file_content: str = TextFileLoader(fr.full_path).load()
                    words_source: WordsSource = WordsSource(fr.full_path, create_words_counter(file_content, is_subtitles))
                    self._words_manager.add_include_words_source(words_source)
                except Exception as e:
                    raise RuntimeError(f"Failed to process '{fr.full_path}' file: \n{str(e)}") from e

            for fr in exclude_files:
                try:
                    is_subtitles: bool = True if fr.name.lower().endswith(".srt") else False
                    file_content: str = TextFileLoader(fr.full_path).load()
                    words_source: WordsSource = WordsSource(fr.full_path, create_words_counter(file_content, is_subtitles))
                    self._words_manager.add_exclude_words_source(words_source)
                except Exception as e:
                    raise RuntimeError(f"Failed to process '{fr.full_path}' file: \n{str(e)}") from e

            self._dirty = False

        return self._words_manager
