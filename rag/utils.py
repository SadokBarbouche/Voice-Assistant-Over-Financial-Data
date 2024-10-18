def add_to_collection(collection, df, embeddings):
    for i, row in df.iterrows():
        question = row['question']
        context = row['context']
        question_embedding = embeddings.embed_query(question)
        collection.add(
            embeddings=[question_embedding],
            documents=[question],
            metadatas=[{"context": context}],
            ids=[f"id_{i}"]
        )

def query_question(user_question, vector_store_from_client, embeddings):
    try:
        results = vector_store_from_client.similarity_search(
            query=user_question,
            k=2
        )
        if not results or len(results) == 0:
            return None, "No similar question found."
        
        most_similar_question = results[0].page_content
        context = results[0].metadata.get('context')
        
        if context:
            return most_similar_question, context
        else:
            return most_similar_question, "No context available in metadata."

    except Exception as e:
        return None, f"An error occurred: {str(e)}"