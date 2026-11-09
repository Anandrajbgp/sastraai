import json
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from backend.embedding import get_embedding

COLLECTION_NAME = "sanatan_scriptures"

def get_qdrant_client():
    client = QdrantClient(path="./qdrant_storage")
    return client

def initialize_collection(client: QdrantClient):
    collections = client.get_collections().collections
    exists = any(c.name == COLLECTION_NAME for c in collections)
    if not exists:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE
            )
        )

def ingest_scriptures():
    client = get_qdrant_client()
    initialize_collection(client)

    data_path = os.path.join(os.path.dirname(__file__), "data", "bhagavad_gita_sample.json")
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        verses = json.load(f)

    points = []
    for idx, verse in enumerate(verses):
        search_blob = verse.get("search_blob", f"{verse['book_name']} Adhyaya {verse['adhyaya']} Verse {verse['verse']} {verse['translation_english']}")
        vector = get_embedding(search_blob)

        points.append(
            models.PointStruct(
                id=idx + 1,
                vector=vector,
                payload=verse
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    print(f"Successfully ingested {len(points)} shlokas into Qdrant collection '{COLLECTION_NAME}'.")

if __name__ == "__main__":
    ingest_scriptures()
