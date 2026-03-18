import requests
from data_loader import load_news_data
from embeddings import generate_embeddings

ENDEE_URL = "http://localhost:8080"

def store_vectors():

    news = load_news_data("data/news.json")
    sample_news = news[:50]

    embeddings = generate_embeddings(sample_news)

    vectors = []

    for text, vector in zip(sample_news, embeddings):

        vectors.append({
            "values": vector.tolist(),
            "metadata": {"text": text}
        })

    response = requests.post(
        f"{ENDEE_URL}/indexes/news_index/vectors",
        json={"vectors": vectors}
    )

    print("Status:", response.status_code)
    print(response.text)


if __name__ == "__main__":
    store_vectors()