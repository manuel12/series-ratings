from django.test import TestCase
from media_ratings.parsers import RottentomatoesMediaPageParser
    
    
class RottentomatoesMediaPageParserTests(TestCase):
    def setUp(self):
        self.rt_url = "https://www.rottentomatoes.com/tv/love_death_robots"  # love, death and robots
        self.parser = RottentomatoesMediaPageParser(self.rt_url)

    def test_soup(self):            
        self.assertIn(
            "This collection of animated short stories spans several genres,",
            str(self.parser.soup))
        self.assertIn(
            "including science fiction, fantasy, horror and comedy. World-class",
            str(self.parser.soup))
        self.assertIn(
            "animation creators bring captivating stories to life in the form of a",
            str(self.parser.soup))
        self.assertIn(
            "unique and visceral viewing experience. The animated anthology series",
            str(self.parser.soup))
        self.assertIn(
            "includes tales that explore alternate histories, life for robots in a",
            str(self.parser.soup))
        self.assertIn(
            "post-apocalyptic city and a plot for world domination by super-intelligent",
            str(self.parser.soup))
        self.assertIn(
            "yogurt. Among the show's executive producers is Oscar-nominated director David Fincher.",
            str(self.parser.soup))

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
        self.assertIn("mop-ratings-wrap__percentage", str(self.parser.get_elem_2()))

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