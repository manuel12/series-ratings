from bs4 import BeautifulSoup
import urllib.request


class Parser():
    score_elem_class_1 = None
    score_elem_class_2 = None

    def __init__(self, url):
        if not url:
            raise TypeError(
                f"Url received was: {url}. Should be a valid url instead. - Aborting initialization...")
        self.url = url
        print(f"-- Opening: {self.url}...")
        self.soup = BeautifulSoup(self._get_page_source(), 'html.parser')

    def _get_page_source(self):
        page = urllib.request.urlopen(self.url)
        return page.read()

    def get_score_elem_1(self):
        try:
            return self.soup.find(self.score_elem_class_2["tag"],
                                  class_=self.score_elem_class_2["class"])
        except Exception as e:
            return None

    def get_score_value_1(self):
        score_elem_1 = self.get_score_elem_1()
        if not score_elem_1:
            return None
        return score_elem_1.text.strip()

    def get_score_elem_2(self):
        try:
            return self.soup.find_all(self.score_elem_class_2["tag"],
                                      class_=self.score_elem_class_2["class"])[1]
        except Exception as e:
            return None

    def get_score_value_2(self):
        score_elem_2 = self.get_score_elem_2()
        if not score_elem_2:
            return None
        return score_elem_2.text.strip()


class IMDbMediaPageParser(Parser):
    score_elem_class_1 = {"tag": "h1",
                          "class": "sc-b73cd867-0 eKrKux"}
    score_elem_class_2 = {"tag": "div",
                          "class": "sc-7ab21ed2-2 kYEdvH"}

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        return float(parsed_value.split("/")[0])

    def get_score_value(self):
        score_value = self.get_score_value_2()
        clean_score_value = self._clean_up_parsed_value(score_value)
        return clean_score_value


class RottentomatoesMediaPageParser(Parser):
    score_elem_class_1 = {"tag": "span",
                          "class": "mop-ratings-wrap__percentage"}
    score_elem_class_2 = {"tag": "span",
                          "class": "mop-ratings-wrap__percentage"}

    def __init__(self, url):
        super().__init__(url)

    def _clean_up_parsed_value(self, parsed_value):
        return int(parsed_value.replace("%", ""))

    def get_tomatometer_value(self):
        tomatometer_value = self.get_score_value_1()
        if tomatometer_value:
            clean_value = self._clean_up_parsed_value(tomatometer_value)
            return clean_value
        return None

    def get_audience_score_value(self):
        audience_value = self.get_score_value_2()

        if audience_value:
            clean_value = self._clean_up_parsed_value(audience_value)
            return clean_value
        return None

    def get_score_value_1(self):
        try:
            tomatometer_score_wrapper = self.soup.select(
              'div.mop-ratings-wrap__half.critic-score')[0]
            tomatometer_score_element = tomatometer_score_wrapper.find(
              "span", "mop-ratings-wrap__percentage")
            return tomatometer_score_element.text.strip()
        except Exception as e:
            return None

    def get_score_value_2(self):
        try:
            audience_score_wrapper = self.soup.select(
              'div.mop-ratings-wrap__half.audience-score')[0]
            audience_score_element = audience_score_wrapper.find(
              "span", "mop-ratings-wrap__percentage")
            return audience_score_element.text.strip()
        except Exception as e:
            return None
