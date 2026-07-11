import os
from dataclasses import dataclass
from enum import Enum

@dataclass
class FileRecord:
    name: str
    full_path: str


class FileListOperation(Enum):
    ADD = 1
    REMOVE = 2
    CLEAR = 3


class FilesListModel:
    def __init__(self):
        self.items: FileRecord = []
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notify_observers(self, operation: FileListOperation, fileRecord: FileRecord | None):
        for observer in self.observers:
            observer.update(operation, fileRecord)

    def add_item(self, file_path: str):
        full_path: str = file_path
        name: str = os.path.basename(file_path)
        fileRecord: FileRecord = FileRecord(name, full_path)
        self.items.append(fileRecord)
        self.notify_observers(FileListOperation.ADD, fileRecord)

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            fileRecord: FileRecord = self.items.pop(index)
            self.notify_observers(FileListOperation.REMOVE, fileRecord)

    def clear_items(self):
        self.items.clear()
        self.notify_observers(FileListOperation.CLEAR, None)

    def get_items(self) -> list[FileRecord]:
        return self.items.copy()

    def get_item_count(self) -> int:
        return len(self.items)

    def get_file_paths(self) -> list[str]:
        """Returns list of full file paths"""
        return [item.full_path for item in self.items]

    def get_file_names(self) -> list[str]:
        """Returns list of just filenames (without path)"""
        return [item.name for item in self.items]