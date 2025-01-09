import yaml
from rag.retriever import Retriever
from rag.generator import Generator
from rag.agent import Agent
from dynaconf import Dynaconf

settings = Dynaconf(
    settings_files=["config.yaml"],
)

if __name__ == "__main__":
    retriever = Retriever()
    generator = Generator()
    agent = Agent(retriever, generator)

    # Add documents to ChromaDB (use your scraped data here)
    documents = [
        {
            "id": "1",
            "text": "Lyrics of song 1",
            "metadata": {"artist": "Artist 1", "song": "Song 1"},
        },
        {
            "id": "2",
            "text": "Lyrics of song 2",
            "metadata": {"artist": "Artist 2", "song": "Song 2"},
        },
    ]
    retriever.add_documents(documents)

    # Query the system
    query = "What are the lyrics of Song 1?"
    answer = agent.answer(query)
    print("Answer:", answer)
