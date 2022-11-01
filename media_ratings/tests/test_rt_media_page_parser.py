from django.test import TestCase
from media_ratings.parsers import RottentomatoesMediaPageParser


class RottentomatoesMediaPageParserTests(TestCase):
    def setUp(self):
        print("RottentomatoesMediaPageParserTests")

        # love, death and robots
        self.rt_url = "https://www.rottentomatoes.com/tv/the-wire"
        self.parser = RottentomatoesMediaPageParser(self.rt_url)

    def test_clean_up_parsed_value(self):
        cleaned_up_value = self.parser._clean_up_parsed_value("94%")
        self.assertTrue(isinstance(cleaned_up_value, int))
        self.assertEqual(cleaned_up_value, 94)

    def test_get_tomatometer_value(self):
        tomatometer_value = self.parser.get_tomatometer_value()
        self.assertTrue(0 < tomatometer_value < 101)

    def test_get_audience_score_value(self):
        audience_score_value = self.parser.get_audience_score_value()
        self.assertTrue(0 < audience_score_value < 101)

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
        self.assertTrue(isinstance(self.parser.get_value_1(), str))
        self.assertTrue("%" in self.parser.get_value_1())
        clean_value = int(self.parser.get_value_1().replace("%", ""))
        self.assertTrue(0 < clean_value < 101)

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
        self.assertTrue(isinstance(self.parser.get_value_2(), str))
        self.assertTrue("%" in self.parser.get_value_2())
        clean_value = int(self.parser.get_value_2().replace("%", ""))
        self.assertTrue(0 < clean_value < 101)

    def test_get_value_2_returns_none_when_elem_not_found(self):
        self.parser.elem_class_2 = {"tag": "div",
                                    "class": "non-existant-class"}
        self.assertIsNone(self.parser.get_value_2())
