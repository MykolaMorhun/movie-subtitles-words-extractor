import unittest

from app.backend.subtitles_processor import create_words_counter


class TestWordsCounter(unittest.TestCase):

    def test_should_count_words(self):
        test_cases = [
            ("should process empty string","", {}),
            ("should process whitespace string", " ", {}),
            ("should process whitespace string with tabs",
                "  \t ", {}),
            ("should process whitespace string with tabs and new lines",
                "  \t \n\t \n  \t ", {}),
            ("should count words",
                "test it ti it test it",
                {"test": 2, "it": 3, "ti": 1}),
            ("should count words ignore case",
                "Test iT Ti It tEst it",
                {"test": 2, "it": 3, "ti": 1}),
            ("should ignore numbers", "1234", {}),
            ("should ignore several numbers", "83674 4539", {}),
            ("should ignore several numbers in between words",
                "From 5 to 4583",
                {"from": 1, "to": 1}),
            ("should remove tags",
                "Some <i>italic </i> text",
                {"some": 1, "italic": 1, "text": 1}),
            ("should keep text in brackets",
                "Some <more words> here Some [more words] here Some (more words) here Some {more words} here",
                {"some": 4, "more": 4, "words": 4, "here": 4}),
            ("should remove non words",
                "3.14 + 3/4 * x = a/b, where a = 23.56 and b = -x",
                {"where": 1, "and": 1}),
            ("should split words in bad formatted text",
                "one.two one,two one;two one:two one!two one?two one,.two one...two",
                {"one": 8, "two": 8}),
            ("should split words by non spaces",
                "This\"is\"100%open=source,isn't?it(true)",
                {"this": 1, "is": 1, "open": 1, "source": 1, "isn't": 1, "it": 1, "true": 1}),
            ("should ignore subtitles time patters and numbers",
             """
123
01:12:41,581 --> 01:12:48,279
Some text here

124
01:13:00,010 --> 01:14:18,135
Another text here
             """,
             {"some": 1, "text": 2, "here": 2, "another": 1}),
        ]

        for description, input, expected in test_cases:
            with self.subTest(description=description):
                result = dict(create_words_counter(input))
                self.assertDictEqual(result, expected, f"For '{input}' expected '{expected}', but got {result}")


    def test_words_trim(self):
        test_cases = [
            ("should trim spaces", "  test  ", "test"),
            ("should trim tabs", "\t\ttest\t\t", "test"),
            ("should trim period", "Test.", "test"),
            ("should trim comma", "Test,", "test"),
            ("should trim question mark", "Test?", "test"),
            ("should trim exclamation mark", "Test!", "test"),
            ("should trim punctuation symbols", "test,.:;", "test"),
            ("should trim non word characters", "test.,()[]{}:;!?'\"+-_&@", "test"),
            ("should trim non word characters repeated from both sides",
             "'+-—#$%~*@^1234567890’”“`…test'+-—#$%~*@^1234567890’”“`…", "test"),
        ]

        for description, input, expected in test_cases:
            with self.subTest(description=description):
                result = dict(create_words_counter(input))
                self.assertEqual(len(result), 1, f"For '{input}' expected non empty result")
                processed = list(result.keys())[0]
                self.assertEqual(processed, expected, f"For '{input}' expected '{expected}', but got {processed}")


    def test_english_words_normalization(self):
        test_cases = [
            ("should remove possesive case",
                "Jack's", "jack"),
            ("should remove ordinal number",
                "12th", ""),
            ("should remove ordinal number with dash",
                "12-th", ""),
        ]

        for description, input, expected in test_cases:
            with self.subTest(description=description):
                result = dict(create_words_counter(input))
                if not expected:
                    self.assertEqual(len(result), 0)
                    continue
                self.assertEqual(len(result), 1, f"For '{input}' expected non empty result")
                processed = list(result.keys())[0]
                self.assertEqual(processed, expected, f"For '{input}' expected '{expected}', but got {processed}")



if __name__ == "__main__":
    unittest.main()
