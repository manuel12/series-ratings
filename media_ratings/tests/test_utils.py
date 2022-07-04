from django.test import TestCase
from media_ratings.utils import capitalize_phrase, sanitize_phrase, standardize_phrase, raise_attribute_error_if_missing


class CapitalizePhraseTests(TestCase):
    def test_capitalize_phrase_one(self):
        phrase = "hello, world"
        self.assertEqual(capitalize_phrase(phrase), "Hello, World")

    def test_capitalize_phrase_two(self):
        phrase = "foo bar"
        self.assertEqual(capitalize_phrase(phrase), "Foo Bar")

    def test_capitalize_phrase_three(self):
        phrase = "the brown fox jumps over the lazy dog"
        self.assertEqual(capitalize_phrase(phrase),
                         "The Brown Fox Jumps Over The Lazy Dog")


class SanitizePhraseTests(TestCase):
    def test_sanitize_phrase_one(self):
        phrase = "main-slug-1"
        self.assertEqual(sanitize_phrase(phrase), "main slug 1")

    def test_sanitize_phrase_two(self):
        phrase = "user-profile-data"
        self.assertEqual(sanitize_phrase(phrase), "user profile data")

    def test_sanitize_phrase_three(self):
        phrase = "love, death & robots"
        self.assertEqual(sanitize_phrase(phrase), "love, death and robots")


class StandardizePhraseTests(TestCase):
    def test_standardize_phrase_one(self):
        phrase = "main-slug-1"
        self.assertEqual(standardize_phrase(phrase), "Main Slug 1")

    def test_standardize_phrase_two(self):
        phrase = "user-profile-data"
        self.assertEqual(standardize_phrase(phrase), "User Profile Data")

    def test_standardize_phrase_three(self):
        phrase = "the-brown-fox-jumps-over-the-lazy-dog"
        self.assertEqual(standardize_phrase(phrase),
                         "The Brown Fox Jumps Over The Lazy Dog")


class RaiseAttributeErrorIfMissingTests(TestCase):
    def test_raise_attribute_error_if_missing_one(self):
        with self.assertRaises(AttributeError):
            capitalize_phrase()

    def test_raise_attribute_error_if_missing_two(self):
        with self.assertRaises(AttributeError):
            sanitize_phrase()

    def test_raise_attribute_error_if_missing_three(self):
        with self.assertRaises(AttributeError):
            standardize_phrase()

    def test_raise_attribute_error_if_missing_fourth(self):
        with self.assertRaises(AttributeError):
            raise_attribute_error_if_missing()
