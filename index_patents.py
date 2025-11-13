import json
import os
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
ELASTIC_URL = os.getenv("ELASTIC_URL")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
ELASTIC_INDEX = os.getenv("ELASTIC_INDEX", "patents")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# --- Sample Data File ---
DATA_PATH = "sample_patents.json"  # JSON file with [{'title': ..., 'abstract': ..., 'url': ...}, ...]

# --- Initialize Clients ---
es = Elasticsearch(ELASTIC_URL, api_key=ELASTIC_API_KEY)
model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# --- Create Index (if not exists) ---
if not es.indices.exists(index=ELASTIC_INDEX):
    es.indices.create(index=ELASTIC_INDEX, body={
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "abstract": {"type": "text"},
                "url": {"type": "keyword"},
                "embedding": {"type": "dense_vector", "dims": 384}  # Adjust if using a different embedding model
            }
        }
    })

# --- Load and Index Data ---
with open(DATA_PATH, "r") as f:
    docs = json.load(f)

for doc in tqdm(docs, desc="Indexing patents"):
    text = f"{doc['title']} {doc['abstract']}"
    embedding = model.encode(text).tolist()
    doc_body = {
        "title": doc["title"],
        "abstract": doc["abstract"],
        "url": doc.get("url", ""),
        "embedding": embedding
    }
    es.index(index=ELASTIC_INDEX, body=doc_body)

