from django.test import TestCase
from media_ratings.utils import capitalize_phrase, sanitize_phrase, standardize_phrase, raise_attribute_error_if_missing


class UtilsTests(TestCase):
    def setUp(self):
        self.phrase = "hello-world"
        
    def test_capitalize_phrase(self):
        capitalized_phrase = capitalize_phrase(self.phrase)
        self.assertEqual(capitalized_phrase, "Hello-world")
    
    def test_sanitize_phrase(self):
        sanitized_phrase = sanitize_phrase(self.phrase)
        self.assertEqual(sanitized_phrase, "hello world")
    
    def test_standardize_phrase(self):
        standardized_phrase = standardize_phrase(self.phrase)
        self.assertEqual(standardized_phrase, "Hello World")
    
    def test_raise_attribute_error_if_missing(self):
        with self.assertRaises(AttributeError):
            raise_attribute_error_if_missing()