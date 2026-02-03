import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
#from langchain.schema import Document
from langchain_core.documents import Document

# 1. Configuration - Ensure these paths match your Docker volume mappings
INDEX_PATH = "data/faiss_index"


def get_rag_context(query: str, k: int = 4) -> str:
    """
    Retrieves the most relevant context from the local vector database
    based on the user's query.
    """
    try:
        # Load the embedding model (2026 standard is high-efficiency models)
        embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Load the existing FAISS index from your local data folder
        if not os.path.exists(INDEX_PATH):
            return "No context available. Please sync your data first."

        vector_db = FAISS.load_local(
            INDEX_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )

        # Perform a similarity search to find the 'k' most relevant chunks
        # This uses mathematical vector calculations to find conceptually similar text
        docs = vector_db.similarity_search(query, k=k)

        # Combine the retrieved content into a single context string
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    except Exception as e:
        print(f"Error retrieving RAG context: {e}")
        return "An error occurred during context retrieval."


def index_documents(documents: List[Document]):
    """
    Utility function to create or update the vector store with new PDFs.
    """
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_db = FAISS.from_documents(documents, embeddings)
    vector_db.save_local(INDEX_PATH)
    print(f"Successfully indexed {len(documents)} document chunks.")
