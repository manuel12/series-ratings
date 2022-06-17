from .parsers import Parser

class SearchResultsParser(Parser):
    search_url_prefix = ""
    search_url_suffix = ""
    search_result_elem_cls = ""

    no_results_text = ""
    no_results_cls = ""

    def __init__(self, search_query):
        self.search_query = search_query
        self.url = self.search_url_prefix + self.search_query + self.search_url_suffix
        self.url = self._clean_up_url(self.url)
        super().__init__(self.url)

    def _clean_up_url(self, url):
        print(f"-- Cleaning url: {url}...")
        return url.strip().replace(" ", "+").replace("-", "+")

    def validate_search_result_text(self, search_result_text):
        search_query_words = self.search_query.split(" ")
        all_words_present_on_text = True

        for word in search_query_words:
            if not word in search_result_text:
                all_words_present_on_text  = False
        return all_words_present_on_text


    def get_search_results(self):
        """Returns an array of search result elements."""
        return self.soup.find_all(class_=self.search_result_elem_cls)

    def get_search_urls(self):
        """Returns an array of href's from search results."""
        return [url.find('a')['href'] for url in self.get_search_results()]

    def get_first_search_result_url(self):
        """Returns the complete url for the first search result."""
        search_result_url = self.get_search_urls()[0]
        return search_result_url

    def get_first_search_result_text(self):
        """Returns the text for the first search result."""
        first_search_result_text = self.get_search_results()[0].find('a').text.strip()
        return first_search_result_text

    def no_results_found(self):        
        return True if len(self.get_search_results()) == 0 else False


class IMDBSearchResultsParser(SearchResultsParser):
    search_url_prefix = "https://www.imdb.com/search/title/?title="
    search_url_suffix = "&languages=en"
    search_result_elem_cls = "lister-item-header"

    """https://www.imdb.com/search/title/?title=breaking+bad&languages=en"""
    
    no_results_text = "No results found for"
    no_results_cls = "findHeader"

    def get_search_results(self):
        return self.soup.find_all(class_=self.search_result_elem_cls)

    def get_search_urls(self):
        return [url.find('a')['href'] for url in self.get_search_results()]

    def get_first_search_result_text(self):
        first_search_result_text = self.get_search_results()[0].find('a').text.strip()
        return first_search_result_text

    def get_first_search_result_url(self):
        search_result_url = f"https://www.imdb.com{self.get_search_urls()[0]}"
        return search_result_url

    def get_search_result_url(self):
        if self.no_results_found():
            return False

        search_result_text = self.get_first_search_result_text()
        if not self.validate_search_result_text(search_result_text):
            return False
        return self.get_first_search_result_url()

    def no_results_found(self):
        return True if len(self.get_search_results()) == 0 else False


class RottentomatoesSearchResultsParser(SearchResultsParser):
    search_url_prefix = "https://www.rottentomatoes.com/search?search="
    search_result_elem_cls = "search-page-media-row"
    
    no_results_text = "Sorry, no results found for"
    no_results_cls = "js-search-no-results-title search__no-results-header"

    def get_tv_search_results_section(self):
        try:
            page_result_section = self.soup.find_all("search-page-result")[1]
            if page_result_section.find('h2').get_text() == "TV shows":
                return page_result_section
            else:
                page_result_section = self.soup.find_all(
                    "search-page-result")[2]
                if page_result_section.find('h2').get_text() == "TV shows":
                    return page_result_section
        except IndexError:
            return self.soup.find_all("search-page-result")[1]

    def get_tv_search_results(self):
          tv_search_results_section = self.get_tv_search_results_section()
          tv_search_results = tv_search_results_section.find_all(
              "search-page-media-row")
          return tv_search_results

    def get_tv_search_results_urls(self):
        tv_search_results = self.get_tv_search_results()
        return [tv_url.find('a')['href'] for tv_url in tv_search_results]

    def get_first_search_result_text(self):
        first_search_result_text = self.get_tv_search_results()[0].find_all('a')[1].text.strip()
        return first_search_result_text

    def get_first_tv_search_result_url(self):
        tv_search_result_url = self.get_tv_search_results_urls()[0]
        return tv_search_result_url

    def get_search_result_url(self):
        if self.no_results_found():
            return False

        search_result_text = self.get_first_search_result_text()
        if not self.validate_search_result_text(search_result_text):
            return False

        print(f"-- Returning url: {self.get_first_tv_search_result_url()}")
        return self.get_first_tv_search_result_url()

    def no_results_found(self):
        return True if len(self.get_tv_search_results()) == 0 else False