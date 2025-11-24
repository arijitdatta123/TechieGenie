import json
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import OPENAI_API_KEY

def load_documents():
    # 1. Load metadata.json
    metadata_path = os.path.join("vector", "metadata.json")
    with open(metadata_path, "r", encoding="utf-8") as f:
        docs = json.load(f)

    raw_docs = []
    metadatas = []

    for item in docs:
        raw_docs.append(item["text"])
        metadatas.append({"video_id": item.get("video_id")})

    # 2. Split
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )
    chunks = splitter.create_documents(raw_docs, metadatas=metadatas)

    # 3. Embeddings
    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model="text-embedding-3-small"
    )

    # 4. NEW Chroma (correct signature)
    persist_dir = os.path.join("vector", "db")
    os.makedirs(persist_dir, exist_ok=True)

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,     # ⭐ correct argument
        persist_directory=persist_dir,
        collection_name="techiegenie"
    )

    print("✅ Vector DB created successfully!")
    print(f"📁 Saved at: {persist_dir}")

if __name__ == "__main__":
    load_documents()
