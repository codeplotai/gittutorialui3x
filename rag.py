
### web based RAG - Flask

import faiss
import requests
from sentence_transformers import SentenceTransformer
import numpy as np

# Load embedding model
embed_model = SentenceTransformer(
    "all-MiniLM-L6-v2",
    local_files_only=True
)
# Load FAISS index
index = faiss.read_index("faiss_index.index")

# Load stored chunks
with open("chunks.txt", "r", encoding="utf-8") as f:
    chunks = f.readlines()


def ask_rag(question):
    # Embed question
    query_vector = embed_model.encode([question])
    query_vector = np.array(query_vector).astype("float32")

    # Search in FAISS
    D, I = index.search(query_vector, k=1)

    retrieved_text = "\n".join([chunks[i] for i in I[0]])

    final_prompt = f"""
    Use the context below to answer:

    {retrieved_text}

    Question: {question}
    """

    # Call Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": final_prompt,
            "stream": False
        }
    )

    return response.json()["response"]