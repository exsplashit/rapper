import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.utils import embedding_functions


class Retriever:
    def __init__(self, settings):
        """Initialize the Retriever with Dynaconf settings."""
        print(settings.as_dict())  # Debug: Print loaded settings
        self.client = chromadb.PersistentClient(
            path=settings.db.path,  # Path for persistence
            settings=ChromaSettings(
                anonymized_telemetry=False,  # Optional: Disable telemetry
            ),
        )
        self.collection = self.client.get_or_create_collection("song_lyrics")
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key="YOUR_OPENAI_API_KEY"  # Replace with your OpenAI API key
        )

    def add_documents(self, documents):
        """Add documents to ChromaDB."""
        for doc in documents:
            self.collection.add(
                ids=[doc["id"]],
                documents=[doc["text"]],
                metadatas=[doc["metadata"]],
            )

    def retrieve(self, query, n_results=5):
        """Retrieve the most relevant documents."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            embedding_function=self.embedding_function,
        )
        return results["documents"], results["metadatas"]
