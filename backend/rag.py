from qdrant_client import QdrantClient
from backend.embedding import get_embedding
from backend.models import QueryResponse, PramanCitation
from typing import List

COLLECTION_NAME = "sanatan_scriptures"

class SanatanRAGEngine:
    def __init__(self):
        self.client = QdrantClient(path="./qdrant_storage")

    def retrieve(self, query: str, top_k: int = 2) -> List[dict]:
        query_vector = get_embedding(query)
        try:
            results = self.client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=top_k
            )
            return [hit.payload for hit in results]
        except Exception as e:
            print(f"Retrieval error: {e}")
            return []

    def generate_response(self, query: str, language: str = "english") -> QueryResponse:
        retrieved_chunks = self.retrieve(query, top_k=2)

        if not retrieved_chunks:
            return QueryResponse(
                answer_summary="I could not find a direct scriptural reference (Praman) in the indexed scriptures for this specific query.",
                praman_citations=[],
                confidence_score=0.0
            )

        citations = []
        summary_parts = []

        for chunk in retrieved_chunks:
            translation = chunk["translation_hindi"] if language.lower() == "hindi" else chunk["translation_english"]
            citations.append(
                PramanCitation(
                    book_name=chunk["book_name"],
                    book_code=chunk["book_code"],
                    adhyaya=chunk["adhyaya"],
                    verse=chunk["verse"],
                    sanskrit_iast=chunk["sanskrit_iast"],
                    sanskrit_devanagari=chunk["sanskrit_devanagari"],
                    translation=translation
                )
            )
            summary_parts.append(f"According to {chunk['book_name']} (Adhyaya {chunk['adhyaya']}, Verse {chunk['verse']}): {translation}")

        answer_summary = " ".join(summary_parts)

        return QueryResponse(
            answer_summary=answer_summary,
            praman_citations=citations,
            confidence_score=0.95
        )
