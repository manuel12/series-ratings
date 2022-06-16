from .utils import standardize_phrase
from .models import TV_Series, IMDbScores, RottentomatoesScores
from .search_parsers import IMDBSearchResultsParser, RottentomatoesSearchResultsParser
from .parsers import IMDbMediaPageParser, RottentomatoesMediaPageParser


class ScoreManager():
    """
    Class to handle the process of standardizing user's search term, 
    creating a tv series instance if it doesn't already exist, fetching 
    said series's search result urls on IMDb or Rottentomatoes.

    Fetching their score values, creating imdb or rt score model
    instances and saving them to the database.

    And finally returning a dictionary of all the score values.
    """

    def __init__(self, search_term):
        self.imdb_score = "N/A"
        self.rt_tomatometer = "N/A"
        self.rt_audience_score = "N/A"

        self.score_data = {}
        self.score_data["rt"] = {}

        self.complete_data_available = False

        self.search_term = standardize_phrase(search_term)
        print(f"-- Searching for term: {self.search_term}")

        tv_series = TV_Series.objects.filter(title=self.search_term).first()

        if tv_series:
            print(f"-- Found series: {tv_series}")

            self.tv_series = tv_series
            self.imdb_score = tv_series.imdb_scores()["imdb_score"]
            self.rt_tomatometer = tv_series.rottentomatoes_scores()[
                "tomatometer"]
            self.rt_audience_score = tv_series.rottentomatoes_scores()[
                "audience_score"]

            self.score_data["imdb"] = self.imdb_score
            self.score_data["rt"]["tomatometer"] = self.rt_tomatometer
            self.score_data["rt"]["audience_score"] = self.rt_audience_score

            print(
                f"-- {tv_series} has scores: {self.imdb_score, self.rt_tomatometer, self.rt_audience_score}")

            if "N/A" not in (self.imdb_score, self.rt_tomatometer, self.rt_audience_score):
                self.complete_data_available = True
        else:
            self.tv_series = TV_Series.objects.create(title=self.search_term)
            self.tv_series.save()

        print(f"-- complete_data_available: {self.complete_data_available}")

    def get_score_data(self):
        print(f"-- Getting score data")

        if self.complete_data_available:
            print(f"-- Returning score data")
            return self.score_data
        else:
            # Fetch each piece of the missing score data.
            if "N/A" in self.imdb_score:
                print(f"-- Fetching score data for imdb")

                # Fetch imdb score.
                imdb_score_value = self.fetch_score("imdb")

                # Create imdb model instance.
                new_imdb_score = self.create_score_model_instance(
                    "imdb", imdb_score_value)

                # Save imdb model instance to db.
                self.save_model_instance(new_imdb_score)
                self.score_data["imdb"] = f"{imdb_score_value}/10" if imdb_score_value else 'N/A'

            if "N/A" in (self.rt_tomatometer, self.rt_audience_score):
                print(f"-- Fetching score data for rt")

                # Fetch rt score.
                rt_score_values = self.fetch_score("rt")
                print(rt_score_values)

                # Create rt model instance.
                new_rt_score = self.create_score_model_instance("rt",
                                                                rt_score_values["tomatometer"],
                                                                rt_score_values["audience_score"])

                # Save rt model instance to db.
                self.save_model_instance(new_rt_score)

                tomatometer_score = rt_score_values["tomatometer"]
                audience_score = rt_score_values["audience_score"]

                self.score_data["rt"]["tomatometer"] = f"{tomatometer_score}%" if tomatometer_score else 'N/A',
                self.score_data["rt"]["audience_score"] = f"{audience_score}%" if audience_score else 'N/A'

            return self.score_data

    def fetch_score(self, agency):
        if agency == "imdb":
            return self.fetch_score_helper(agency,
                                           IMDBSearchResultsParser,
                                           IMDbMediaPageParser)
        else:
            return self.fetch_score_helper(agency,
                                           RottentomatoesSearchResultsParser,
                                           RottentomatoesMediaPageParser)

    def fetch_score_helper(self, agency, search_result_parser, media_page_parser):
        search_parsers = search_result_parser(self.search_term)
        search_result_url = search_parsers.get_search_result_url()
        page_parser = media_page_parser(search_result_url)
        if agency == "rt":
            score_values = {}
            score_values["tomatometer"] = page_parser.get_tomatometer_value()
            score_values["audience_score"] = page_parser.get_audience_score_value()
            return score_values
        score_value = page_parser.get_score_value()
        return score_value

    def create_score_model_instance(self, agency, score_value_one, score_value_two=None):
        if agency == "imdb":
            new_score = self.create_score_model_instance_helper(IMDbScores,
                                                                media=self.tv_series,
                                                                imdb_score=score_value_one)
        else:
            new_score = self.create_score_model_instance_helper(RottentomatoesScores,
                                                                media=self.tv_series,
                                                                tomatometer_score=score_value_one,
                                                                audience_score=score_value_two)
        print(f"-- Created new {agency} score...")
        return new_score

    def create_score_model_instance_helper(self, scores_model, *args, **kwargs):
        return scores_model.objects.create(*args, **kwargs)

    def save_model_instance(self, model_instance):
        model_instance.save()
        print(f"-- Saved new {model_instance.__class__.__name__} score...")
