from fastapi.testclient import TestClient
from backend.main import app
from backend.ingest import ingest_scriptures
import os

def test_rag_pipeline():
    if not os.path.exists("./qdrant_storage"):
        ingest_scriptures()

    with TestClient(app) as client:
        response = client.get("/")
        print("Root response:", response.status_code, response.json())
        assert response.status_code == 200

        payload = {
            "query": "What does Krishna say about karma and action?",
            "language": "english"
        }
        res = client.post("/api/v1/query", json=payload)
        print("Query response status:", res.status_code)
        print("Query response body:", res.text)
        assert res.status_code == 200
        data = res.json()

        assert "answer_summary" in data
        assert "praman_citations" in data
        assert len(data["praman_citations"]) > 0

        # Verify that at least one citation is from Bhagavad Gita
        citation = data["praman_citations"][0]
        assert citation["book_code"] == "BG"
        assert len(citation["sanskrit_iast"]) > 0
        assert len(citation["sanskrit_devanagari"]) > 0
        assert len(citation["translation"]) > 0

        print("Test passed successfully! All Praman citations verified.")

if __name__ == "__main__":
    test_rag_pipeline()
