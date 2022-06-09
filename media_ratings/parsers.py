from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request


class Parser():
    score_elem_class_1 = None
    score_elem_class_2 = None

    def __init__(self, url):
        if not url:
            raise TypeError(f"Url received was: {url}. Should be a valid url instead. - Aborting initialization...")
        self.url = url
        print(f"-- Opening: {self.url}...")
        self.soup = BeautifulSoup(self._get_page_source(), 'html.parser')
    
    def _get_page_source(self):
        page = urllib.request.urlopen(self.url)
        return page.read()

    def get_score_elem_1(self):
        return self.soup.find(self.score_elem_class_1["tag"],
                              class_=self.score_elem_class_1["class"])

    def get_score_value_1(self):
        if not self.get_score_elem_1():
            return None
        return self.get_score_elem_1().text.strip()

    def get_score_elem_2(self):
        return self.soup.find_all(self.score_elem_class_2["tag"],
                              class_=self.score_elem_class_2["class"])[1]

    def get_score_value_2(self):
        if not self.get_score_elem_2():
            return None
        return self.get_score_elem_2().text.strip()


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
        clean_value = self._clean_up_parsed_value(tomatometer_value)
        return clean_value

    def get_audience_score_value(self):
        audience_value = self.get_score_value_2()
        clean_value = self._clean_up_parsed_value(audience_value)
        return clean_value
