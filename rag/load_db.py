from langchain_chroma import Chroma
from .utils import query_question
from langchain_huggingface import HuggingFaceEmbeddings
import os

embeddings = HuggingFaceEmbeddings(
    model_name="Lajavaness/bilingual-embedding-small", model_kwargs={"trust_remote_code": True}
)

collection_name = "plug-and-tel-assignment-db"
persistant_dir = os.path.join("db", collection_name)


vector_store = Chroma(
    collection_name=collection_name,
    embedding_function=embeddings,
    persist_directory = persistant_dir
)
