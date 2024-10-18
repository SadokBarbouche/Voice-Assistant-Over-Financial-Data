import chromadb
from langchain_chroma import Chroma
import pandas as pd
from .utils import add_to_collection, query_question
from langchain_huggingface import HuggingFaceEmbeddings
import os


if __name__ == "__main__":
    embeddings = HuggingFaceEmbeddings(
        model_name="Lajavaness/bilingual-embedding-small",
        model_kwargs={"trust_remote_code": True},
    )
    collection_name = "plug-and-tel-assignment-db"
    persistant_dir = os.path.join("db", collection_name)

    persistent_client = chromadb.PersistentClient(
        path=persistant_dir,
    )
    collection = persistent_client.get_or_create_collection(collection_name)

    df = pd.read_csv("data/fixed_sujet_dataset.csv")

    vector_store_from_client = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embeddings.embed_query,
        persist_directory=persistant_dir,
    )

    add_to_collection(collection, df, embeddings)
