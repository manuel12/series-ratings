from bs4 import BeautifulSoup
import urllib.request


class Parser():
    elem_class_1 = None
    elem_class_2 = None

    def __init__(self, url="", html_page=""):
        self.html_page = html_page
        if not self.html_page:
            if not url:
                raise TypeError(
                    f"Url received was: {url}. Should be a valid url instead. - Aborting initialization...")
            else:
                self.url = url

        self.soup = BeautifulSoup(self._get_page_source(), 'html.parser')

    def _get_page_source(self):
        if self.html_page:
            return self.html_page

        print(f"-- Opening: {self.url}...")
        page = urllib.request.urlopen(self.url)
        return page.read()

    def get_elem_1(self):
        if not self.elem_class_1:
            raise AttributeError(
                "You need to assign a value to elem_class_1 in order to call this function")
        try:
            return self.soup.find(self.elem_class_1["tag"],
                                  class_=self.elem_class_1["class"])
        except Exception as e:
            return None

    def get_value_1(self):
        score_elem_1 = self.get_elem_1()
        if score_elem_1:
            return score_elem_1.text.strip()
        return None

    def get_elem_2(self):
        if not self.elem_class_2:
            raise AttributeError(
                "You need to assign a value to elem_class_2 in order to call this function")
        try:
            return self.soup.find(self.elem_class_2["tag"],
                                  class_=self.elem_class_2["class"])
        except Exception as e:
            return None

    def get_value_2(self):
        score_elem_2 = self.get_elem_2()
        if score_elem_2:
            return score_elem_2.text.strip()
        return None


class IMDbMediaPageParser(Parser):
    elem_class_1 = {"tag": "div",
                    "class": "sc-7ab21ed2-2 kYEdvH"}
    elem_class_2 = {"tag": "div",
                    "class": "sc-7ab21ed2-2 kYEdvH"}

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        return float(parsed_value.split("/")[0])

    def get_score_value(self):
        score_value = self.get_value_2()
        if score_value:
            clean_score_value = self._clean_up_parsed_value(score_value)
            return clean_score_value
        return None

class RottentomatoesMediaPageParser(Parser):
    elem_class_1 = {"tag": None,
                    "class": "#tomato_meter_link > span > span.mop-ratings-wrap__percentage"}
    elem_class_2 = {"tag": None,
                    "class": "div.mop-ratings-wrap__half.audience-score > h2 > a > span > span.mop-ratings-wrap__percentage"}

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        return int(parsed_value.replace("%", ""))

    def get_tomatometer_value(self):
        tomatometer_value = self.get_value_1()
        if tomatometer_value:
            clean_value = self._clean_up_parsed_value(tomatometer_value)
            return clean_value
        return None

    def get_audience_score_value(self):
        audience_value = self.get_value_2()

        if audience_value:
            clean_value = self._clean_up_parsed_value(audience_value)
            return clean_value
        return None

    def get_elem_1(self):
        if not self.elem_class_1:
            raise AttributeError(
                "You need to assign a value to elem_class_1 in order to call this function")
        try:
            return self.soup.select(self.elem_class_1["class"])[0]
        except Exception as e:
            return None

    def get_elem_2(self):
        if not self.elem_class_2:
            raise AttributeError(
                "You need to assign a value to elem_class_2 in order to call this function")
        try:
            return self.soup.select(self.elem_class_2["class"])[0]
        except Exception as e:
            return None
