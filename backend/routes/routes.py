from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.schemas import DocumentRequest, GenerateResponse
from backend.config import GEMINI_MODEL, MOCK_AI

router = APIRouter()
_generator = None


def get_generator() -> GeminiDocumentGenerator:
    global _generator
    if _generator is None:
        _generator = GeminiDocumentGenerator()
    return _generator


@router.post("/generate", response_model=GenerateResponse)
def generate_document(request: DocumentRequest) -> GenerateResponse:
    try:
        document = get_generator().generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )
        return GenerateResponse(
            document=document,
            model=GEMINI_MODEL,
            mock=MOCK_AI,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
