import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import openai
import os
from dotenv import load_dotenv

# --- Logo URLs ---
#ELASTIC_LOGO = "https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blt34d540ad62a1b5fa/62b1eb6fc748e046df6fa23c/brand-elastic-logo-220x130.png"
#OPENAI_LOGO = "https://seeklogo.com/images/O/openai-logo-8B9BFEDC26-seeklogo.com.png"
#STREAMLIT_LOGO = "https://streamlit.io/images/brand/streamlit-mark-color.png"

from PIL import Image

elastic_logo = Image.open("elastic-logo.png")
uspto_logo = Image.open("uspto-logo.png")

col1, col2, col3 = st.columns([1,2,1])
with col1:
    st.image(elastic_logo, width=120)
#with col2:
 #   st.markdown("<h1 style='text-align: center; margin-bottom:0'>🧠 Ask the Patent Whisperer</h1>", unsafe_allow_html=True)
with col3:
    st.image(uspto_logo, width=120)

#st.markdown("Search and summarize patents using semantic search + RAG")


# --- Load environment variables ---
load_dotenv()

# --- Configuration ---
ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX", "patents")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1")

# --- Initialize Clients ---
es = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)
model = SentenceTransformer(EMBEDDING_MODEL_NAME)
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE

# --- Streamlit UI ---
#st.set_page_config(page_title="Ask the Patent Whisperer", page_icon="🧠", layout="wide")
st.title("Ask the Patent Whisperer")
st.markdown("""
<div style='font-size:18px'>
Semantic & generative search across US Patents. Powered by <b>Elasticsearch</b><br>
<span style='color:#666;'>Search for inventions, summarize trends, or compare patents with AI.</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
   # st.image("Elastic_NV_logo.svg", width=220)
    #st.image(ELASTIC_LOGO, width=120)
   # st.image(OPENAI_LOGO, width=90)
    #st.image(STREAMLIT_LOGO, width=70)
    st.header("ℹ️ About")
    st.write("""
        - Powered by Elastic & OpenAI GPT-4.1
        - Demo for patent search with RAG
        - Built by Abhi (with a little help from a friendly OpenAI)
    """)
    st.markdown("[View on USPTO](https://www.uspto.gov/patents/search/patent-public-search)")
    st.markdown("---")
    st.write("Try questions like:")
    st.code("Patents related to gesture control in AR/VR\nAI for fraud detection\nBiodegradable packaging\nQuantum computing hardware\nWearable health monitoring devices")

query = st.text_input("🔎 What patent do you want to explore?", placeholder="e.g., AI for fraud detection")
top_k = st.slider("How many results?", 1, 10, 5)

if query:
    with st.spinner("Looking for patent wisdom..."):
        # --- Vectorize the query ---
        query_vector = model.encode(query).tolist()

        # --- Perform vector search in Elastic ---
        response = es.search(
            index=ELASTIC_INDEX,
            knn={
                "field": "embedding",
                "k": top_k,
                "num_candidates": 100,
                "query_vector": query_vector
            },
            source=["title", "abstract", "url"]
        )

        hits = response["hits"]["hits"]
        documents = [f"Title: {hit['_source']['title']}\nAbstract: {hit['_source']['abstract']}" for hit in hits]

        # --- Limit text to avoid token overflow ---
        joined_docs = "\n\n".join(documents)
        max_input_tokens = 3000
        if len(joined_docs) > max_input_tokens:
            joined_docs = joined_docs[:max_input_tokens] + "\n..."

        # --- Generate summary/answer with OpenAI ---
        prompt = f"Based on the following patent abstracts, answer the question: {query}\n\n{joined_docs}\n\nAnswer:"

        response = openai.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful patent analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message.content

        st.subheader("📌 Patent Summary")
        st.success(answer)

        st.markdown("## 🗂️ Top Patent Matches")
        for idx, hit in enumerate(hits, 1):
            patent = hit["_source"]
            st.markdown(
                f"""
                <div style='border:1px solid #eee; border-radius:10px; margin:10px 0; padding:15px; background-color:#f9f9f9;'>
                    <b>🔗 <a href=\"{patent.get('url','#')}\" target=\"_blank\">{patent['title']}</a></b>
                    <br>
                    <span style='color:#444;'>{patent['abstract']}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
