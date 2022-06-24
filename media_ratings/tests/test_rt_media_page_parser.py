from django.test import TestCase
from media_ratings.parsers import RottentomatoesMediaPageParser


class RottentomatoesMediaPageParserTests(TestCase):
    def setUp(self):
        # love, death and robots
        self.rt_url = "https://www.rottentomatoes.com/tv/love_death_robots"
        self.parser = RottentomatoesMediaPageParser(self.rt_url)

    def test_clean_up_parsed_value(self):
        cleaned_up_value = self.parser._clean_up_parsed_value("93%")
        self.assertEqual(cleaned_up_value, 93)

    def test_get_tomatometer_value(self):
        tomatometer_value = self.parser.get_tomatometer_value()
        self.assertEqual(tomatometer_value, 85)

    def test_get_audience_score_value(self):
        audience_score_value = self.parser.get_audience_score_value()
        self.assertEqual(audience_score_value, 78)

    def test_get_elem_1(self):
        self.assertIn("mop-ratings-wrap__percentage",
                      str(self.parser.get_elem_1()))

    def test_elem_class_1_not_assigned_error(self):
        self.parser.elem_class_1 = None
        with self.assertRaises(AttributeError):
            self.parser.get_elem_1()

    def test_get_elem_1_returns_none_when_elem_not_found(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_elem_1())

    def test_get_value_1(self):
        self.assertEqual(self.parser.get_value_1(), "85%")

    def test_get_value_1_returns_none_when_elem_not_found(self):
        self.parser.elem_class_1 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_value_1())

    def test_get_elem_2(self):
        self.assertIn("mop-ratings-wrap__percentage",
                      str(self.parser.get_elem_2()))

    def test_elem_class_2_not_assigned_error(self):
        self.parser.elem_class_2 = None
        with self.assertRaises(AttributeError):
            self.parser.get_elem_2()

    def test_get_elem_2_returns_none_when_elem_not_found(self):
        self.parser.elem_class_2 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_elem_2())

    def test_get_value_2(self):
        self.assertEqual(self.parser.get_value_2(), "78%")

    def test_get_value_2_returns_none_when_elem_not_found(self):
        self.parser.elem_class_2 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_value_2())
