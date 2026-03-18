import json

def load_news_data(file_path):
    
    articles = []

    with open(file_path, "r") as f:
        for line in f:
            data = json.loads(line)

            text = data["headline"] + " " + data["short_description"]

            articles.append(text)

    return articles


if __name__ == "__main__":
    
    news = load_news_data("data/news.json")

    print("Total articles:", len(news))
    print("Example article:", news[0])