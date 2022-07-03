import json


def load_json_data(file):
    with open(file) as f:
        data = json.load(f)
    return data


def save_json_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)


def capitalize_phrase(phrase):
    raise_attribute_error_if_missing(phrase)
    return " ".join([word.capitalize() for word in phrase.split(" ")])


def sanitize_phrase(phrase):
    raise_attribute_error_if_missing(phrase)
    return "".join(char.replace("&", "and").replace("-", " ") for char in phrase)


def standardize_phrase(phrase):
    return capitalize_phrase(sanitize_phrase(phrase))


def raise_attribute_error_if_missing(phrase=None):
    if not phrase:
        raise AttributeError("The search term cannot be empty.")
