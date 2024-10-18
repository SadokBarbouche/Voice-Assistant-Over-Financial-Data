from langchain_huggingface import HuggingFaceEmbeddings
from .utils import query_question
from .load_db import vector_store

if __name__ == "__main__":
    print(vector_store._collection.count())
    embeddings = HuggingFaceEmbeddings(
        model_name="Lajavaness/bilingual-embedding-small",
        model_kwargs={"trust_remote_code": True},
    )

    user_question = "Quel est le chiffre d'affaires total du Groupe Air France-KLM pour l'année 2023 ?"
    most_similar_question, fetched_context = query_question(
        user_question, vector_store, embeddings
    )
    print("Most similar question:", most_similar_question)
    print("Equivalent context:", fetched_context)
