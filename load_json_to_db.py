from dynaconf import Dynaconf
from rag.retriever import Retriever

# Initialize Dynaconf with explicit settings file
settings = Dynaconf(settings_files=["settings.yaml"])


def load_json_files_to_db(input_dir):
    """Load JSON files from a directory and populate the database."""
    import os
    import json

    documents = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(input_dir, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Prepare document
            doc = {
                "id": f"{data['artist']}_{data['song_name']}".replace(" ", "_"),
                "text": data["lyrics"],
                "metadata": {
                    "artist": data["artist"],
                    "song_name": data["song_name"],
                    "year": data.get("year", "Unknown"),
                    **data.get("metadata", {}),
                },
            }
            documents.append(doc)

    return documents


def main():
    # Ensure the directory exists
    input_dir = settings.scrape.output_dir
    retriever = Retriever(settings)  # Pass the Dynaconf settings instance

    # Load documents from JSON files
    documents = load_json_files_to_db(input_dir=input_dir)

    # Add documents to the database
    if documents:
        retriever.add_documents(documents)
        print(f"Successfully added {
              len(documents)} document(s) to the database.")
    else:
        print("No documents found to add to the database.")


if __name__ == "__main__":
    main()
