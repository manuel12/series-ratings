from django.test import TestCase
from media_ratings.parsers import Parser


class ParserTests(TestCase):
    def setUp(self):
        self.google_url = "https://www.google.com/"
        self.imdb_url = "https://www.imdb.com/title/tt9561862/"  # love, death and robots
        # love, death and robots
        self.rt_url = "https://www.rottentomatoes.com/tv/love_death_robots"

    def test_url_cannot_be_false(self):
        with self.assertRaises(TypeError):
            url = False
            parser = Parser(url)

    def test_page_source(self):
        url = "https://www.google.com/"
        parser = Parser(url)
        self.assertInHTML("<title>Google</title>", str(parser._get_page_source()))

    def test_soup(self):
        url = "https://www.google.com/"
        parser = Parser(url)
        self.assertIn("<title>Google</title>", str(parser.soup))

    def test_get_elem_1(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_1 = {"tag": "div",
                                     "class": "sc-7ab21ed2-2 kYEdvH"}

        self.assertIn("hero-rating-bar__aggregate-rating__score",
                      str(parser.get_elem_1()))
        
    def test_elem_class_1_not_assigned_error(self):
        with self.assertRaises(AttributeError):
            parser = Parser(self.imdb_url)
            parser.get_elem_1()

    def test_get_elem_1_returns_none_when_elem_not_found(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_1 = {"tag": "div",
                                     "class": "non-existant-class"}
        self.assertIsNone(parser.get_elem_1())


    def test_get_value_1(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_1 = {"tag": "div",
                                     "class": "sc-7ab21ed2-2 kYEdvH"}

        self.assertEqual(parser.get_value_1(), "8.4/10")
    
    def test_get_value_1_returns_none_when_elem_not_found(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_1 = {"tag": "div",
                                     "class": "non-existant-class"}
        self.assertIsNone(parser.get_value_1())

    def test_get_elem_2(self):
        parser = Parser(self.rt_url)
        parser.elem_class_2 = {"tag": "span",
                                     "class": "mop-ratings-wrap__percentage"}
        self.assertIn("mop-ratings-wrap__percentage", str(parser.get_elem_2()))

    def test_elem_class_2_not_assigned_error(self):
        with self.assertRaises(AttributeError):
            parser = Parser(self.imdb_url)
            parser.get_elem_2()
    
    def test_get_elem_2_returns_none_when_elem_not_found(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_2 = {"tag": "div",
                                     "class": "non-existant-class"}
        self.assertIsNone(parser.get_elem_2())

    def test_get_value_2(self):
        parser = Parser(self.rt_url)
        parser.elem_class_2 = {"tag": "span",
                                     "class": "mop-ratings-wrap__percentage"}

        self.assertEqual(parser.get_value_2(), "78%")
    
    def test_get_value_2_returns_none_when_elem_not_found(self):
        parser = Parser(self.imdb_url)
        parser.elem_class_2 = {"tag": "div",
                                     "class": "non-existant-class"}
        self.assertIsNone(parser.get_value_2())