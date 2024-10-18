from langchain_community.document_loaders import HuggingFaceDatasetLoader
import pandas as pd
import os

dataset_name = "sujet-ai/Sujet-Financial-RAG-FR-Dataset"
data = None
csv_path = "data/sujet_dataset.csv"
question_column = "question"
context_column = "context"

question_loader = HuggingFaceDatasetLoader(dataset_name, page_content_column=question_column)
context_loader = HuggingFaceDatasetLoader(dataset_name, page_content_column=context_column)

questions = question_loader.load()
context = context_loader.load()


if not os.path.exists(csv_path):
    data = list(zip([question.page_content for question in questions],[ctx.page_content for ctx in context]))
    data = pd.DataFrame(data, columns=[question_column, context_column])
    data.to_csv(csv_path, index=False)