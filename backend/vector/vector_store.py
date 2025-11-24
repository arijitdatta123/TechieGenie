import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY

def get_vector_store():
    persist_dir = os.path.join("vector", "db")

    embeddings = OpenAIEmbeddings(
        api_key=OPENAI_API_KEY,
        model="text-embedding-3-small"
    )

    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings,
        collection_name="techiegenie"
    )

    return db
