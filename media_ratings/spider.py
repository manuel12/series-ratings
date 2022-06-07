from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from .utils import load_json_data, save_json_data

json_data = load_json_data("media_ratings/temp-data.json")
rating_data = {
    "metacritic": {},
    "imdb": {},
    "rottentomatoes": {}
}


class RatingSpider(Spider):
    name = 'rating'
    start_urls = [
        'https://www.metacritic.com/tv/stranger-things',
        'https://www.imdb.com/title/tt4574334/?ref_=nv_sr_srsg_0',
        'https://www.rottentomatoes.com/tv/stranger_things'
    ]

    def parse(self, response):

        if("imdb" in response.url):
            imdb_element = response.css(".sc-7ab21ed2-1::text")
            self._print("imdb", imdb_element)
            self._set_rating_data(rating_data, "imdb", imdb_element)

        if("metacritic" in response.url):
            metascore_element = response.css('.metascore_w::text')[19]
            self._print("metascore", metascore_element)
            self._set_rating_data(rating_data, "metascore", metascore_element)

            user_score_element = response.css(".metascore_w::text")[20]
            self._print("userscore", user_score_element)
            self._set_rating_data(rating_data, "userscore", user_score_element)

        if("rottentomatoes" in response.url):
            tomatometer_element = response.css('.mop-ratings-wrap__percentage::text')[0]
            self._print("tomatometer", tomatometer_element)
            self._set_rating_data(rating_data, "tomatometer", tomatometer_element)
            
            audience_score_element = response.css('.mop-ratings-wrap__percentage::text')[1]
            self._print("audience_score", audience_score_element)
            self._set_rating_data(rating_data, "audience_score", audience_score_element)

        print("-------------------------------------------------------")
        print(rating_data)
        print("-------------------------------------------------------")
        save_json_data("media_ratings/temp-data.json", json_data)

    def _get_text_from_element(self, elem):
        return elem.get().strip()

    def _set_rating_data(self, rating_data, rating_agency, rating_element):
        rating_value = self._get_text_from_element(rating_element)

        if(rating_agency == "imdb"):
            rating_data[rating_agency] = rating_value

        elif(rating_agency == "metascore"):
            rating_data["metacritic"]["metascore"] = rating_value
        elif(rating_agency == "userscore"):
            rating_data["metacritic"]["user_score"] = rating_value

        elif(rating_agency == "tomatometer"):
            rating_data["rottentomatoes"]["tomatometer"] = rating_value
        elif(rating_agency == "audience_score"):
            rating_data["rottentomatoes"]["audience_score"] = rating_value

        json_data.update(rating_data)

    def _print(self, page, data):
        data = self._get_text_from_element(data)

if __name__=="__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    process.crawl(RatingSpider)
    process.start()
