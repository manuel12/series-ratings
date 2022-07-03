from .parsers import Parser


class SearchResultsParser(Parser):
    """
    Class used to extract search results from a given search engine.
    Extends Parser.

    Should not be used directly but extended instead.

    It takes in 2 params:
        search_query: a query to be submitted to search engines.
        html_page: a string representing markup.
    If html_page is provided it will skip using url altogether.

    It forms a url by concatenating search_url_prefix, search_query and search_url_suffix
    together and cleaning them up. Then it passes that url to the parent class, along with
    a html_page markup string, if provided.

    For class variables:
        search_url_prefix   = "https://www.google.com/search?q="
        search_query        = "python documentation"
        search_url_suffix   = "&hl=en"

    The url formed will be:
        https://www.google.com/search?q=python+documentation&hl=en


    Specify the html class atribute to use as locator for search results
    by assinging a class name to search_result_elem_cls.

    For a markup such as:
    <html>
        <body>
            <div class="found-search-results">
                <div class="search-result"></div>
                <div class="search-result"></div>
                <div class="search-result"></div>
                <div class="search-result"></div>
            </div>

        </body>
    </html>

    The search_result_elem_cls should be:
        search_result_elem_cls = "found-search-results"

    """
    search_url_prefix = ""
    search_url_suffix = ""
    search_result_elem_cls = ""

    should_validate_search_result = False

    def __init__(self, search_query, html_page=""):
        self.search_query = search_query
        if not self.search_query:
            raise ValueError("You need to assign a value to search_query!")
        self.url = self.search_url_prefix + self.search_query + self.search_url_suffix
        self.url = self._clean_up_url(self.url)
        super().__init__(self.url, html_page)

    def _clean_up_url(self, url):
        """
        Returns a clean url string.
        Url before cleaning: https://www.imdb.com/title/love death and-robots/
        Url after cleaning: https://www.imdb.com/title/love+death+and+robots/
        """
        print(f"-- Cleaning url: {url}...")
        return url.strip().replace(" ", "+").replace("-", "+")

    def get_search_results(self):
        """Returns an array of search result elements."""
        return self.soup.find_all(class_=self.search_result_elem_cls)

    def get_search_urls(self):
        """Returns an array of href's from search results."""
        return [url.find('a')['href'] for url in self.get_search_results()]

    def get_first_search_result_url(self):
        """Returns the complete url for the first search result."""
        search_result_urls = self.get_search_urls()
        if search_result_urls:
            search_result_url = self.get_search_urls()[0]
            return search_result_url
        else:
            return None

    def get_first_search_result_text(self):
        """Returns the text for the first search result."""
        search_result_urls = self.get_search_urls()
        if search_result_urls:
            first_search_result_text = self.get_search_results()[
                0].find('a').text.strip()
            return first_search_result_text
        else:
            return None

    def get_search_result_url(self):
        """Returns the href from the first search result, None if not found."""
        if self.no_results_found():
            return None

        return self.get_first_search_result_url()

    def no_results_found(self):
        """Returns True if get_search_results returns an empty list, False otherwise."""
        return True if len(self.get_search_results()) == 0 else False


class IMDBSearchResultsParser(SearchResultsParser):
    """Class used to extract results elements, urls and text from IMDb search."""
    search_url_prefix = "https://www.imdb.com/search/title/?title="
    search_url_suffix = "&languages=en"
    search_result_elem_cls = "lister-item-header"

    def get_first_search_result_url(self):
        """Returns the complete imdb url for the first search result."""
        super_search_result_url = super().get_first_search_result_url()
        if super_search_result_url:
            search_result_url = f"https://www.imdb.com{super_search_result_url}"
            return search_result_url
        else:
            None


class RottentomatoesSearchResultsParser(SearchResultsParser):
    """Class used to extract results elements, urls and text from Rottentomatoes search."""

    search_url_prefix = "https://www.rottentomatoes.com/search?search="
    search_result_elem_cls = "search-page-media-row"

    def _get_search_results_sections(self):
        return self.soup.find_all("search-page-result")

    def get_tv_search_results_section(self):
        """
        Returns the element that contains all the search results of the TV section
        as opposed to the movies and actors setion.
        """
        try:
            page_sections = self.soup.find_all("search-page-result")
            for section in page_sections:
                if 'type="tv"' in str(section):
                    return section
        except IndexError:
            return self.soup.find_all("search-page-result")[0]

    def get_search_results(self):
        """Returns an array of search result elements."""
        tv_search_results_section = self.get_tv_search_results_section()
        search_results = tv_search_results_section.find_all(
            self.search_result_elem_cls)
        return search_results

    def get_first_search_result_text(self):
        """Returns the text for the first search result."""
        search_result_urls = self.get_search_urls()
        if search_result_urls:
            first_search_result_text = self.get_search_results()[0].find_all('a')[
                1].text.strip()
            return first_search_result_text
        else:
            return None
