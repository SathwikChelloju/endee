import streamlit as st
from embeddings import generate_embeddings
import requests

# ---------------- CONFIG ----------------
ENDEE_URL = "http://localhost:8080"
API_KEY = "pub_7d98ea6eac324be2943db44f1d543f22"

# ---------------- NEWS API ----------------
def fetch_news(query):

    url = f"https://newsdata.io/api/1/news?apikey={API_KEY}&q={query}&language=en"

    try:
        response = requests.get(url, timeout=10).json()
    except:
        return []

    articles = []

    if response.get("status") == "success":

        for art in response.get("results", [])[:6]:

            articles.append({
                "title": art.get("title"),
                "description": art.get("description"),
                "content": art.get("content"),
                "image": art.get("image_url"),
                "url": art.get("link")
            })

    return articles


# ---------------- ENDEE SEARCH ----------------
def search_vectors(query_vector):

    response = requests.post(
        f"{ENDEE_URL}/index/default/search",
        json={
            "vector": query_vector.tolist(),
            "top_k": 5
        }
    )

    if response.status_code == 200:
        return response.json()

    return None


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI News Recommendation",
    page_icon="📰",
    layout="wide"
)

# ---------------- STYLE ----------------
st.markdown("""
<style>
.big-title {
    font-size:42px !important;
    font-weight:800;
    text-align:center;
    color:#4ea8de;
}
.subtitle {
    text-align:center;
    color:#94a3b8;
    margin-bottom:25px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown('<p class="big-title">📰 AI News Recommendation System</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover similar news articles using AI embeddings</p>', unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Settings")

st.sidebar.info("""
This system uses:

• Sentence Transformers  
• Endee Vector Database  
• Semantic Search  
• NewsData API
""")

# ---------------- SEARCH ----------------
query = st.text_input(
    "🔎 Enter a news topic",
    placeholder="Example: AI, war, world cup, covid"
)

st.divider()

# ---------------- TRENDING ----------------
if not query:

    st.subheader("🔥 Trending News Today")

    trending_articles = fetch_news("world")

    if not trending_articles:
        st.warning("Unable to load trending news.")

    for art in trending_articles[:5]:

        if art["image"]:
            st.image(art["image"], use_container_width=True)

        st.markdown(f"### {art['title']}")

        if art["description"]:
            st.write(art["description"])

        st.markdown(f"[Read full article]({art['url']})")

        st.divider()


# ---------------- RECOMMENDATION ----------------
if query:

    st.subheader("📌 Your Query")
    st.info(query)

    # Generate embedding
    query_embedding = generate_embeddings([query])[0]

    # Search in Endee
    results = search_vectors(query_embedding)

    st.subheader("✨ AI Recommended Articles")

    # Fetch real articles
    articles = fetch_news(query)

    if not articles:
        st.warning("No articles found.")

    for art in articles:

        if art["image"]:
            st.image(art["image"], use_container_width=True)

        st.markdown(f"### {art['title']}")

        if art["description"]:
            st.write(art["description"])

        if art["content"]:
            st.write(art["content"])

        st.markdown(f"[Read full article]({art['url']})")

        st.divider()

st.caption("🚀 Built with SentenceTransformers + Endee Vector Database")