from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    query: str = Field(..., description="User question in English, Hindi, or Sanskrit")
    language: Optional[str] = Field("english", description="Preferred response language: english, hindi, sanskrit")

class PramanCitation(BaseModel):
    book_name: str = Field(..., description="Name of the scripture, e.g., Bhagavad Gita")
    book_code: str = Field(..., description="Standard book code, e.g., BG")
    adhyaya: int = Field(..., description="Chapter or Adhyaya number")
    verse: int = Field(..., description="Verse or Shloka number")
    sanskrit_iast: str = Field(..., description="Original Sanskrit text in IAST transliteration")
    sanskrit_devanagari: str = Field(..., description="Original Sanskrit text in Devanagari script")
    translation: str = Field(..., description="Translation in the requested response language")

class QueryResponse(BaseModel):
    answer_summary: str = Field(..., description="Synthesis answering the user's question grounded strictly in scripture")
    praman_citations: List[PramanCitation] = Field(..., description="Mandatory list of verified Praman references supporting the answer")
    confidence_score: float = Field(..., description="Retrieval and verification confidence score between 0.0 and 1.0")
