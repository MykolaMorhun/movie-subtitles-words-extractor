from collections import Counter
from dataclasses import dataclass

@dataclass
class WordsSource:
    key: str
    words_counter: Counter[str]


class WordsManager:
    """
    Process words sources to get resulting words.
    """

    def __init__(self):
        self._dirty: bool = True

        self._include_words_sources: dict[str, WordsSource] = dict()
        self._exclude_words_sources: dict[str, WordsSource] = dict()
        self._result: Counter[str]


    def add_include_words_source(self, ws: WordsSource) -> None:
        """Adds a new words source to include into the result."""
        self._dirty = True
        self._include_words_sources[ws.key] = ws


    def remove_include_words_source(self, ws: WordsSource) -> None:
        """Removes a words source from include sources."""
        self._dirty = True
        self._include_words_sources.pop(ws.key)


    def clear_include_words(self) -> None:
        self._dirty = True
        self._include_words_sources = dict()


    def add_exclude_words_source(self, ws: WordsSource) -> None:
        """Adds a new words source to exclude from the result."""
        self._dirty = True
        self._exclude_words_sources[ws.key] = ws


    def remove_exclude_words_source(self, ws: WordsSource) -> None:
        """Removes a words source from exclude sources."""
        self._dirty = True
        self._exclude_words_sources.pop(ws.key)


    def clear_exclude_words(self) -> None:
        self._dirty = True
        self._exclude_words_sources = dict()


    @staticmethod
    def _merge_word_sources(sources: dict[str, WordsSource]) -> Counter[str]:
        """
        Merges all include or exclude word sources in a way that sums words occurance.
        """
        words_counter: Counter[str] = Counter()
        for ws in sources.values():
            words_counter += ws.words_counter
        return words_counter


    def _calculate_result(self):
        """
        Merges all include sources and extracts all exclude sources.
        """
        self._dirty = False

        positive_merged = self._merge_word_sources(self._include_words_sources)
        negative_merged = self._merge_word_sources(self._exclude_words_sources)

        result = positive_merged
        for word in negative_merged:
            result.pop(word, None)

        self._result = result


    def get_words_counter(self) -> Counter[str]:
        """
        Returns unique words counts.
        Formed from words from the positive sources excluding words from negative sources.
        """
        if self._dirty:
            self._calculate_result()
        return self._result


    def get_words_dict(self) -> dict[str, int]:
        """
        Returns dictionary of unique words which key is a word and the value is the number of the word occurance in sources.
        The dictionary is formed from words from the positive sources excluding words from negative sources.
        """
        return dict(self.get_words_counter())


    def get_words_list(self) -> list[str]:
        """
        Returns alphabetically sorted list of unique words.
        The list is formed from words from the positive sources excluding words from negative sources.
        """
        all_words_list: list[str] = list(self.get_words_dict().keys())
        all_words_list.sort()
        return all_words_list


    def get_words_string(self) -> str:
        """
        Returns alphabetically sorted list of unique words as a single multiline string.
        """
        return "\n".join(self.get_words_list())
