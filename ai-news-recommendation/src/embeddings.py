from sentence_transformers import SentenceTransformer
from data_loader import load_news_data

# load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(texts):

    embeddings = model.encode(texts)

    return embeddings


if __name__ == "__main__":

    news = load_news_data("data/news.json")

    # take only first 100 articles for testing
    sample_news = news[:100]

    vectors = generate_embeddings(sample_news)

    print("Total vectors:", len(vectors))
    print("Vector size:", len(vectors[0]))