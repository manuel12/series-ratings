from django.test import TestCase
from media_ratings.parsers import Parser

html_page = """
<html>
    <head><title>Mock Page</title></head>
    <body>
        <div class="score-element-one" data-test="rating-score-one">
            9.7/10
        </div>
        <div>
            <span class="score-element-two-wrapper">
                <div class="score-element-two">
                    93%
                </div>
            </span>
        </div>
    </body>
</html>
"""


class ParserTests(TestCase):
    def setUp(self):
        self.parser = Parser(html_page=html_page)

    def test_url_cannot_be_false(self):
        with self.assertRaises(TypeError):
            url = False
            parser = Parser(url)

    def test_get_page_source(self):
        self.assertInHTML("<title>Mock Page</title>",
                          str(self.parser._get_page_source()))

    def test_soup(self):
        self.assertIn("<title>Mock Page</title>", str(self.parser.soup))

    def test_get_elem_1(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "score-element-one"}

        self.assertIn("rating-score-one",
                      str(self.parser.get_elem_1()))

    def test_elem_class_1_not_assigned_error(self):
        with self.assertRaises(AttributeError):

            self.parser.get_elem_1()

    def test_get_elem_1_returns_none_when_elem_not_found(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_elem_1())

    def test_get_value_1(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "score-element-one"}

        self.assertEqual(self.parser.get_value_1(), "9.7/10")

    def test_get_value_1_returns_none_when_elem_not_found(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_value_1())

    def test_get_elem_2(self):
        self.parser.elem_class_2 = {"tag": "span",
                                    "class": "score-element-two-wrapper"}
        self.assertIn("score-element-two", str(self.parser.get_elem_2()))

    def test_elem_class_2_not_assigned_error(self):
        with self.assertRaises(AttributeError):

            self.parser.get_elem_2()

    def test_get_elem_2_returns_none_when_elem_not_found(self):
        self.parser.elem_class_2 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_elem_2())

    def test_get_value_2(self):
        self.parser.elem_class_2 = {"tag": "span",
                                    "class": "score-element-two-wrapper"}

        self.assertEqual(self.parser.get_value_2(), "93%")

    def test_get_value_2_returns_none_when_elem_not_found(self):
        self.parser.elem_class_2 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_value_2())
