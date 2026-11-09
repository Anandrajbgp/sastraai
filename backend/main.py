from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from backend.models import QueryRequest, QueryResponse
from backend.rag import SanatanRAGEngine
from backend.ingest import ingest_scriptures
import os

rag_engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global rag_engine
    if not os.path.exists("./qdrant_storage"):
        ingest_scriptures()
    rag_engine = SanatanRAGEngine()
    yield

app = FastAPI(
    title="Sanatan Shastra AI API",
    version="1.0.0",
    description="Zero-hallucination scriptural querying platform anchored in authentic Praman.",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "Sanatan Shastra AI API",
        "message": "Om Shanti. Ask questions grounded in Vedas, Upanishads, and Bhagavad Gita."
    }

@app.post("/api/v1/query", response_model=QueryResponse)
def query_scriptures(request: QueryRequest):
    try:
        response = rag_engine.generate_response(request.query, request.language)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
