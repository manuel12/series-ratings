from .utils import standardize_phrase
from .models import TV_Series, IMDbScores, RottentomatoesScores
from .parse_imdb_score import get_imdb_score
from .parse_rt_score import get_rt_scores


def get_score_data(search_term):
    imdb_score = "N/A"
    rt_tomatometer_score = "N/A"
    rt_audience_score = "N/A"

    score_data = {
        "imdb": imdb_score,
        "rt": {
            "tomatometer": rt_tomatometer_score,
            "audience_score": rt_audience_score
        }
    }

    complete_data_available = False

    search_term = standardize_phrase(search_term)
    print(f"-- Searching for term: {search_term}")

    tv_series = TV_Series.objects.filter(title=search_term).first()
    print(f"-- tv_series: {tv_series}")

    if(tv_series):
        # Get imdb and rt score data from existing tv series model
        print(f"-- Found series: {tv_series}")

        imdb_score = tv_series.imdb_scores()["imdb_score"]
        rt_tomatometer_score = tv_series.rottentomatoes_scores()[
            "tomatometer"]
        rt_audience_score = tv_series.rottentomatoes_scores()[
            "audience_score"]

        score_data["imdb"] = imdb_score
        score_data["rt"]["tomatometer"] = rt_tomatometer_score
        score_data["rt"]["audience_score"] = rt_audience_score
    else:
        tv_series = TV_Series.objects.create(title=search_term)
        tv_series.save()

    print(f"-- Getting score data")
    print(f"-- Title: {tv_series.title}")

    if complete_data_available:
        print(f"-- Returning score data")
        return score_data
    else:
        # Fetch each piece of the missing score data.
        if "N/A" == imdb_score:
            print(f"-- Fetching score data for imdb")

            # Fetch imdb score.
            imdb_score_value = get_imdb_score(search_term)
            print(f"-- imdb_score_value: {imdb_score_value}")

            # Create imdb model instance.
            existing_score_model = IMDbScores.objects.filter(
                media=tv_series).first()
            if existing_score_model:
                print(
                    f"-- Score model already exists for tv_series: {tv_series}")
                print(f"-- Deleting score model: {existing_score_model}")
                existing_score_model.delete()

            print(
                f"-- Created new {IMDbScores.__class__.__name__} score...")
            new_imdb_score_model = IMDbScores.objects.create(
                media=tv_series, imdb_score=imdb_score_value)

            print(f"-- new_imdb_score_model: {new_imdb_score_model}")

            score_data["imdb"] = new_imdb_score_model.imdb_score

        if "N/A" in (rt_tomatometer_score, rt_audience_score):
            print(f"-- Fetching score data for rt")

            # Fetch rt score.
            rt_score_values = get_rt_scores(search_term)
            print(f"-- rt_score_values: {rt_score_values}")

            # Create rt model instance.
            existing_score_model = RottentomatoesScores.objects.filter(
                media=tv_series).first()
            if existing_score_model:
                print(
                    f"-- Score model already exists for tv_series: {tv_series}")
                print(f"-- Deleting score model: {existing_score_model}")
                existing_score_model.delete()

            print(
                f"-- Created new {RottentomatoesScores.__class__.__name__} score...")
            new_rt_score_model = RottentomatoesScores.objects.create(
                media=tv_series,
                tomatometer_score=rt_score_values["tomatometer"],
                audience_score=rt_score_values["audience_score"])

            score_data["rt"] = {
                "tomatometer": new_rt_score_model.tomatometer_score,
                "audience_score": new_rt_score_model.audience_score
            }

        return score_data, search_term
