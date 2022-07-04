from bs4 import BeautifulSoup
import urllib.request
import validators


class Parser:
    """
    Class used to extract elements and values from a html markup.

    Should not be used directly but extended instead.

    It takes in 2 params:
        url: a valid url.
        html_page: a string representing markup.
    If html_page is provided it will skip using url altogether.

    It can extract 2 elements and 2 values.
    For this purpose it exposes 4 methods:
        get_elem_1, get_value_1, get_elem_2, get_value_2

    Specify html tags and class atributes to
    use as locators by assinging a dict to either elem_class_1 or
    elem_class_2.

    For a markup such as:
    <html>
        <body>
            <div class="element-1"></div>
            <span class="element-2"></span>
        </body>
    </html>

    The dict for elem_class_1 should be as follows:
    elem_class_1 = {
        "tag": "div",
        "class": "element-1"
    }

    And the dict for elem_class_2 should be as follows:
    elem_class_2 = {
        "tag": "span",
        "class": "element-2"
    }
    """

    elem_class_1 = None
    elem_class_2 = None

    def __init__(self, url="", html_page=""):
        self.html_page = html_page
        if not self.html_page:
            if not url or not validators.url(url):
                raise TypeError(
                    f"Url received was: {url}. Should be a valid url instead. - Aborting initialization...")
            else:
                self.url = url

        self.soup = BeautifulSoup(self._get_page_source(), 'html.parser')

    def _get_page_source(self):
        """Return of html_page markup or if not read page source from url."""
        if self.html_page:
            return self.html_page

        print(f"-- Opening: {self.url}...")
        page = urllib.request.urlopen(self.url)
        return page.read()

    def get_elem_1(self):
        """Return element from locators specified on elem_class_1 or None if not found."""
        if not self.elem_class_1:
            raise AttributeError(
                "You need to assign a dict with tag and class values to elem_class_1 in order to call this function")
        try:
            return self.soup.find(self.elem_class_1["tag"],
                                  class_=self.elem_class_1["class"])
        except Exception as e:
            return None

    def get_value_1(self):
        """Return stripped text from element returned by get_elem_1."""
        elem_1 = self.get_elem_1()
        if elem_1:
            return elem_1.text.strip()
        return None

    def get_elem_2(self):
        """Return element from locators specified on elem_class_2 or None if not found."""
        if not self.elem_class_2:
            raise AttributeError(
                "You need to assign a dict with tag and class values to elem_class_2 in order to call this function")
        try:
            return self.soup.find(self.elem_class_2["tag"],
                                  class_=self.elem_class_2["class"])
        except Exception as e:
            return None

    def get_value_2(self):
        """Return stripped text from element returned by get_elem_2."""
        elem_2 = self.get_elem_2()
        if elem_2:
            return elem_2.text.strip()
        return None


class IMDbMediaPageParser(Parser):
    """
    Class used to extract the IMDb(https://www.imdb.com/) Rating
    value from a specific media(Example: tv series) page.

    Extends Parser.
    """

    # imdb score element.
    elem_class_1 = {
        "tag": "div",
        "class": "sc-7ab21ed2-2 kYEdvH"
    }

    elem_class_2 = {
        "tag": "div",
        "class": "sc-7ab21ed2-2 kYEdvH"
    }

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        """
        Returns a float value by cleaning the IMDb Rating string:
            IMDb Rating => "8.4/10"
            Clean value: 8.4
        """
        return float(parsed_value.split("/")[0])

    def get_score_value(self):
        """Returns the clean IMDb score value or None if not found."""
        score_value = self.get_value_1()
        if score_value:
            clean_score_value = self._clean_up_parsed_value(score_value)
            return clean_score_value
        return None


class RottentomatoesMediaPageParser(Parser):
    """
    Class used to extract the Rottentomatoes(https://www.rottentomatoes.com/)
    tomatometer and audience score values from a specific media
    (Example: tv series) page.

    Extends Parser.
    """

    # tomatometer score element.
    elem_class_1 = {
        "tag": None,
        "class": "#tomato_meter_link > span > span.mop-ratings-wrap__percentage"
    }

    # audience score element.
    elem_class_2 = {
        "tag": None,
        "class": "div.mop-ratings-wrap__half.audience-score > h2 > a > span > span.mop-ratings-wrap__percentage"
    }

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        """
        Returns an int value by cleaning the Rottentomatoes tomatometer
        or audience score string:
            Tomatometer/Audience Score => "97%"
            Clean value: 97
        """
        return int(parsed_value.replace("%", ""))

    def get_tomatometer_value(self):
        """Returns the clean tomatometer value or None if not found."""
        tomatometer_value = self.get_value_1()
        if tomatometer_value:
            clean_value = self._clean_up_parsed_value(tomatometer_value)
            return clean_value
        return None

    def get_audience_score_value(self):
        """Returns the clean audience score value or None if not found."""
        audience_value = self.get_value_2()
        if audience_value:
            clean_value = self._clean_up_parsed_value(audience_value)
            return clean_value
        return None

    def get_elem_1(self):
        """
        Overrides Parser.get_elem_2 as Rottentomatoes requires a slightly different element
        location strategy.
        """
        if not self.elem_class_1:
            raise AttributeError(
                "You need to assign a value to elem_class_1 in order to call this function")
        try:
            return self.soup.select(self.elem_class_1["class"])[0]
        except Exception as e:
            return None

    def get_elem_2(self):
        """
        Overrides Parser.get_elem_2 as Rottentomatoes requires a slightly different element
        location strategy.
        """
        if not self.elem_class_2:
            raise AttributeError(
                "You need to assign a value to elem_class_2 in order to call this function")
        try:
            return self.soup.select(self.elem_class_2["class"])[0]
        except Exception as e:
            return None
