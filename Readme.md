🧠 Ask the Patent Whisperer

A demo app that combines semantic search and RAG (Retrieval-Augmented Generation) to make patent discovery effortless. Users can ask natural language questions and receive summarized insights from actual patent abstracts.

🚀 Features

Semantic vector search using Elasticsearch

Sentence embedding with sentence-transformers

RAG-style summarization with GPT-4.1 via OpenAPI-compatible proxy

Streamlit UI for a fast, interactive experience

🧱 Setup Instructions

1. Clone the repo and install dependencies

pip install -r requirements.txt

2. Environment Variables

Create a .env file or export the following variables:

ELASTIC_URL=https://searchai-standdeliver-f9c7bf.es.us-east-1.aws.elastic.cloud:443
ELASTIC_INDEX=patents
EMBEDDING_MODEL=all-MiniLM-L6-v2
ELASTIC_API_KEY=VU5iT0U1Z0JEU0kxcXZETWRTeUI6S2xBWWszZmhmdF9GTkFfdXBZVDVVdw==
OPENAI_API_KEY=sk-NDaRFQXb8pY7SOT5myTTlg
OPENAI_MODEL=gpt-4.1
OPENAI_API_BASE=https://litellm-proxy-service-1059491012611.us-central1.run.app/v1/chat/completions

In your Python code, configure the OpenAI client like this:

import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

Elasticsearch setup:

from elasticsearch import Elasticsearch

es = Elasticsearch(
    os.getenv("ELASTIC_URL"),
    api_key=os.getenv("ELASTIC_API_KEY")
)

3. Start the app

streamlit run app.py

4. (Optional) Index sample data

python index_patents.py

📦 requirements.txt

streamlit
elasticsearch
sentence-transformers
openai
python-dotenv
tqdm

📂 Suggested Folder Structure

patent-whisperer/
├── app.py                    # Main Streamlit app
├── index_patents.py          # Script to load and index sample data
├── sample_patents.json       # Mock data for testing
├── .env.example              # Template for environment variables
├── requirements.txt          # Dependencies
├── README.md
└── .gitignore                # Exclude sensitive or unneeded files

📄 .gitignore

.env
__pycache__/
*.pyc
.DS_Store
.streamlit/

📌 Example Questions

"Patents related to gesture control in AR/VR"

"Which patents use renewable energy for medical devices?"

"Who owns the most patents in drone swarming?"

🧠 How It Works

User enters a question

Query is embedded into a dense vector

Top-K similar patent abstracts are retrieved from Elasticsearch

GPT-4.1 summarizes them into a human-friendly answer

📄 Patent Data Requirements

Your Elasticsearch index (patents) should contain at least the following fields:

title: Patent title

abstract: Patent abstract

embedding: Dense vector embedding of the text

url (optional): Link to the patent on USPTO or Google Patents

🙌 Credits

Built with ❤️ using Elastic, Sentence Transformers, OpenAPI-compatible LLMs, and Streamlit.

Got a feature idea or data source in mind? PRs welcome!

# 🧠 Ask the Patent Whisperer

A demo app that combines **semantic search** and **RAG (Retrieval-Augmented Generation)** to make patent discovery effortless. Users can ask natural language questions and receive summarized insights from actual patent abstracts.

---

## 🚀 Features
- Semantic vector search using Elasticsearch
- Sentence embedding with `sentence-transformers`
- RAG-style summarization with GPT-4.1 via OpenAPI-compatible proxy
- Streamlit UI for a fast, interactive experience

---

## 🧱 Setup Instructions

### 1. Clone the repo and install dependencies
```bash
pip install -r requirements.txt

