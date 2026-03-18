import requests
from data_loader import load_news_data
from embeddings import generate_embeddings

ENDEE_URL = "http://localhost:8080"

def recommend_news():

    news = load_news_data("data/news.json")

    query_text = news[0]

    query_embedding = generate_embeddings([query_text])[0]

    response = requests.post(
        f"{ENDEE_URL}/indexes/news_index/search",
        json={
            "vector": query_embedding.tolist(),
            "top_k": 5
        }
    )

    print("Query Article:\n")
    print(query_text)

    print("\nResults from Endee:\n")
    print(response.text)

if __name__ == "__main__":
    recommend_news()