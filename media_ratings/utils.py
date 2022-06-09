import json

def load_json_data(file):
    with open(file) as f:
      data = json.load(f)
    return data


def save_json_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f)
        

def capitalize_phrase(phrase):
    return " ".join([word.capitalize() for word in phrase.split(" ")])

def sanitize_phrase(phrase):
    return "".join(char.replace("&", "and").replace("-", " ") for char in phrase)

def standardize_phrase(phrase):
    return capitalize_phrase(sanitize_phrase(phrase))

def start_crawler_process(spider):
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings

    settings = get_project_settings()
    print(settings)
    print("------------------------------------------------------------")
    process = CrawlerProcess(settings)
    process.crawl(spider)
    process.start()
    