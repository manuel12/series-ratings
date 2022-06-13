from .parsers import Parser

class SearchResultsParser(Parser):
    search_url_prefix = ""
    search_url_suffix = ""
    
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

    def get_search_results(self):
        """Returns an array of search result elements."""
        pass

    def get_search_urls(self):
        """Returns an array of href's from search results."""
        pass

    def get_first_search_result_url(self):
        """Returns the complete url for the first search result."""
        pass
    
    def no_results_found(self):        
        no_results_element = self.soup.find(class_=self.no_results_cls)
        if no_results_element and self.no_results_text in no_results_element.get_text():
            return True


class IMDBSearchResultsParser(SearchResultsParser):
    search_url_prefix = "https://www.imdb.com/find?q="
    search_url_suffix = "&ref_=nv_sr_sm"
    search_result_elem_cls = "result_text"
    
    no_results_text = "No results found for"
    no_results_cls = "findHeader"

    def get_search_results(self):
        return self.soup.find_all(class_=self.search_result_elem_cls)

    def get_search_urls(self):
        return [url.find('a')['href'] for url in self.get_search_results()]

    def get_first_search_result_url(self):
        search_result_url = f"https://www.imdb.com{self.get_search_urls()[0]}"
        return search_result_url

    def get_search_result_url(self):
        if self.no_results_found():
            return False
        print(f"-- Returning url: {self.get_first_search_result_url()}")
        return self.get_first_search_result_url()


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

    def get_tv_search_results_urls(self):
        tv_search_results_section = self.get_tv_search_results_section()
        tv_search_results = tv_search_results_section.find_all(
            "search-page-media-row")
        return [tv_url.find('a')['href'] for tv_url in tv_search_results]

    def get_first_tv_search_result_url(self):
        tv_search_result_url = self.get_tv_search_results_urls()[0]
        return tv_search_result_url

    def get_search_result_url(self):
        if self.no_results_found():
            return False
        print(f"-- Returning url: {self.get_first_tv_search_result_url()}")
        return self.get_first_tv_search_result_url()